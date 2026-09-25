-- Metabolic Free: lead/client pipeline + decision evidence log (Postgres / Supabase)
-- Health answers live ONLY here (BAA-covered storage). Never sync them to ad platforms.

create type segment as enum ('weight_energy', 'prediabetic', 'type2', 'glp1', 'hormones', 'performance');
create type stage as enum ('lead', 'nurturing', 'call_booked', 'call_showed', 'enrolled',
                           'active', 'paused', 'churned', 'lost', 'referred_out');

create table contacts (
  id               uuid primary key default gen_random_uuid(),
  created_at       timestamptz not null default now(),
  first_name       text,
  email            text unique,
  phone            text,
  state_region     text,               -- decides telehealth eligibility
  timezone         text,
  -- consent (separate flags, with evidence)
  email_consent_at timestamptz,
  sms_consent_at   timestamptz,
  consent_ip       inet,
  -- attribution
  utm_source       text,
  utm_campaign     text,
  utm_content      text,               -- ad / creative id
  referred_by      uuid references contacts(id),
  -- scoring
  metabolic_score  int check (metabolic_score between 0 and 100),
  segment          segment,
  red_flag         boolean not null default false,  -- route to physician, notify coach
  stage            stage not null default 'lead',
  stage_changed_at timestamptz not null default now()
);

create table quiz_answers (
  contact_id  uuid references contacts(id) on delete cascade,
  question    text not null,
  answer      text not null,
  answered_at timestamptz not null default now()
);

create table enrollments (
  id                 uuid primary key default gen_random_uuid(),
  contact_id         uuid references contacts(id),
  plan               text not null,          -- 'coaching_monthly', 'coaching_6mo', 'group'
  price_per_month    numeric(10,2) not null,
  telehealth_addon   boolean not null default false,
  commitment_months  int not null default 6,
  lumen_shipped_at   timestamptz,
  started_at         date not null,
  ended_at           date,
  end_reason         text
);

create table sessions (
  id            uuid primary key default gen_random_uuid(),
  enrollment_id uuid references enrollments(id),
  scheduled_for timestamptz not null,
  status        text not null default 'scheduled',  -- scheduled | attended | no_show | rescheduled
  adherence     int check (adherence between 1 and 5),
  notes         text
);

-- The decision layer: every agent action, why it was taken, and what actually happened.
create table decision_log (
  id              bigserial primary key,
  created_at      timestamptz not null default now(),
  agent           text not null,        -- content | ads | nurture | booking | retention | reporting | outreach
  action          text not null,        -- e.g. 'pause_adset', 'send_sms', 'publish_post'
  target          text,                 -- ad set id, contact id, post id
  rationale       text not null,
  expected_metric text,                 -- e.g. 'blended_cpl'
  expected_value  numeric,
  policy_result   text not null,        -- passed | blocked:<rule> | needs_approval
  approved_by     text,                 -- 'auto' or coach
  executed        boolean not null default false,
  actual_value_7d  numeric,
  actual_value_30d numeric,
  verdict         text                  -- helped | neutral | hurt (filled by reporting agent)
);

-- Weekly funnel view (feeds the 1-page report)
create view weekly_funnel as
select date_trunc('week', created_at) as week,
       utm_campaign,
       count(*)                                                      as leads,
       count(*) filter (where stage not in ('lead','nurturing','lost','referred_out')) as booked,
       count(*) filter (where stage in ('enrolled','active','paused','churned')) as enrolled
from contacts
group by 1, 2;
