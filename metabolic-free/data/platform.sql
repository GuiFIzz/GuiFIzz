-- Metabolic Free client platform (Supabase). Apply as a migration.
-- Scope: coaching and lifestyle data only. Medication, prescriptions and medical records live
-- in Altrohealth (GFC Lab) and are NEVER stored here.

create table if not exists profiles (
  id            uuid primary key references auth.users(id) on delete cascade,
  role          text not null default 'client' check (role in ('client', 'coach')),
  first_name    text,
  start_date    date,                       -- program week 1 starts here
  next_session  timestamptz,
  plan          text default 'foundation',  -- foundation ($299 x 3) | momentum ($199 x 6)
  active        boolean not null default true,
  created_at    timestamptz not null default now()
);

create table if not exists checkins (
  client_id     uuid not null references profiles(id) on delete cascade,
  day           date not null,
  lumen_score   int check (lumen_score between 1 and 5),   -- Lumen: 1 = burning fat ... 5 = burning carbs
  weight_lb     numeric(5,1),
  protein_hit   boolean,
  steps         int,
  walk_done     boolean,
  sleep_hours   numeric(3,1),
  energy        int check (energy between 1 and 5),
  note          text,
  created_at    timestamptz not null default now(),
  primary key (client_id, day)
);

create table if not exists workout_logs (
  client_id     uuid not null references profiles(id) on delete cascade,
  week          int not null check (week between 1 and 52),
  day           text not null check (day in ('A', 'B', 'C')),
  done_at       timestamptz not null default now(),
  primary key (client_id, week, day)
);

-- Coach check without recursive RLS
create or replace function is_coach() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from profiles where id = auth.uid() and role = 'coach');
$$;

-- Public founding-spot counter for the website (returns a number only, no personal data)
create or replace function spots_taken() returns int
language sql stable security definer set search_path = public as $$
  select count(*)::int from profiles where role = 'client' and active and start_date is not null;
$$;
grant execute on function spots_taken() to anon, authenticated;

alter table profiles     enable row level security;
alter table checkins     enable row level security;
alter table workout_logs enable row level security;

create policy "own profile read"    on profiles for select using (id = auth.uid() or is_coach());
create policy "coach edits profiles" on profiles for update using (is_coach());
create policy "own checkins"        on checkins for all using (client_id = auth.uid() or is_coach())
                                    with check (client_id = auth.uid());
create policy "own workouts"        on workout_logs for all using (client_id = auth.uid() or is_coach())
                                    with check (client_id = auth.uid());

-- New sign-ups get a client profile automatically (the coach sets start_date on enrollment)
create or replace function handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into profiles (id, first_name) values (new.id, new.raw_user_meta_data->>'first_name');
  return new;
end $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function handle_new_user();
