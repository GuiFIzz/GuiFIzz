// Hulk: the GFC Xtreme AI assistant widget. Self-injecting — include this one script tag
// on any page and the floating button + chat panel appear. Talks to functions/api/hulk.js.
(function () {
  const esc = (window.MF && MF.esc) || ((s) => String(s));
  const endpoint = (window.MF_CONFIG && MF_CONFIG.HULK_ENDPOINT) || "/api/hulk";
  const history = []; // {role, content}

  document.body.insertAdjacentHTML("beforeend", `
    <button id="hulkBtn" type="button" aria-haspopup="dialog" aria-expanded="false">💪 Ask Hulk</button>
    <div id="hulkPanel" role="dialog" aria-label="Chat with Hulk">
      <div id="hulkHead">
        <div><b>Hulk</b><span>GFC Xtreme AI · ask me about the program</span></div>
        <button id="hulkClose" type="button" aria-label="Close chat">×</button>
      </div>
      <div id="hulkMsgs"></div>
      <p class="hulkNote">AI assistant, not medical advice. For anything clinical, <a href="lab.html">GFC Lab</a> has you covered.</p>
      <form id="hulkForm">
        <textarea id="hulkInput" rows="1" placeholder="Ask about pricing, the program, Lumen..." required></textarea>
        <button id="hulkSend" type="submit">Send</button>
      </form>
    </div>`);

  const btn = document.getElementById("hulkBtn");
  const panel = document.getElementById("hulkPanel");
  const msgs = document.getElementById("hulkMsgs");
  const form = document.getElementById("hulkForm");
  const input = document.getElementById("hulkInput");
  const send = document.getElementById("hulkSend");

  function addBubble(role, text) {
    const row = document.createElement("div");
    row.className = `hulkRow ${role === "user" ? "user" : "bot"}`;
    row.innerHTML = `<div class="hulkBubble">${esc(text)}</div>`;
    msgs.appendChild(row);
    msgs.scrollTop = msgs.scrollHeight;
    return row;
  }

  let opened = false;
  btn.onclick = () => {
    panel.classList.toggle("on");
    const isOpen = panel.classList.contains("on");
    btn.setAttribute("aria-expanded", String(isOpen));
    if (isOpen && !opened) {
      opened = true;
      addBubble("bot", "Hey, I'm Hulk — the GFC Xtreme AI. Ask me anything about the Metabolic Flex program: pricing, what's included, Lumen, GFC Lab, how it works. I'll answer what I can and point you to a real call for anything that needs a human.");
      input.focus();
    }
  };
  document.getElementById("hulkClose").onclick = () => { panel.classList.remove("on"); btn.setAttribute("aria-expanded", "false"); };

  form.onsubmit = async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    addBubble("user", text);
    history.push({ role: "user", content: text });
    input.value = ""; input.style.height = "auto";
    send.disabled = true; input.disabled = true;
    const thinking = addBubble("bot", "…");
    try {
      const r = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history }),
      });
      const data = await r.json();
      const reply = data.ok && data.reply ? data.reply : "I'm having trouble answering right now — want to just book a free call instead? https://cal.com/gfcxtreme-fitness-nmylwf/30min";
      thinking.querySelector(".hulkBubble").textContent = reply;
      history.push({ role: "assistant", content: reply });
    } catch (err) {
      thinking.querySelector(".hulkBubble").textContent = "Something went wrong on my end — try again, or book a free call: https://cal.com/gfcxtreme-fitness-nmylwf/30min";
    }
    send.disabled = false; input.disabled = false; input.focus();
    msgs.scrollTop = msgs.scrollHeight;
  };

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
  });
  input.addEventListener("input", () => {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 100) + "px";
  });
})();
