HEADER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

html, body, .stApp, .block-container, .main {
  //background-color: #f5f3eb !important;
  direction: rtl;
  text-align: right;
}

.stChatInput input {
  text-align: right;
}

.signature {
  font-family: 'Great Vibes', cursive;
  font-size: 60px;
  stroke: black;
  stroke-width: 1px;
  fill: transparent;
  animation: draw 3s ease forwards;
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
}

@keyframes draw {
  to {
    stroke-dashoffset: 0;
    fill: #2c2c2c;
  }
}

hr.full-divider {
  border: none;
  border-top: 1px solid #bbb;
  margin-top: 0.5rem;
  margin-bottom: 2rem;
  width: 100%;
}
</style>

<div style="text-align: center; margin-bottom: 5px;">
  <svg viewBox="0 0 600 150" width="300" height="75">
    <text x="50%" y="90" text-anchor="middle" class="signature">הסוכן החכם של ג'אקו</text>
  </svg>
</div>
<hr class="full-divider">
"""