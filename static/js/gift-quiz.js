/* Gift quiz: runs entirely in the browser, sends nothing anywhere.
   Product names, links and claims come from the build (data-products on
   #gift-quiz), which in turn come from data/products.yaml and
   data/gift_meta.yaml, so there is nothing to keep in sync here except
   which product id each answer combination points at. */
(function () {
  var root = document.getElementById("gift-quiz");
  if (!root) return;

  var products;
  try {
    products = JSON.parse(root.getAttribute("data-products") || "{}");
  } catch (e) {
    return;
  }

  var form = root.querySelector(".quiz-form");
  var out = root.querySelector(".quiz-result");

  // [primary, alternative-or-null] for each answer combination.
  function choose(where, exp, budget) {
    if (where === "indoors") return ["hylukon-drift-car", null];
    if (where === "water") {
      if (budget === "low") return ["bezgar-tx126", "bezgar-tx123"];
      return ["bezgar-tx123", "arris-jet-boat"];
    }
    if (where === "air") {
      if (exp === "some" && budget === "high") return ["volantex-ranger600", "volantex-sport-cub"];
      if (budget === "low") return ["hawks-work-glider", "volantex-sport-cub"];
      return ["volantex-sport-cub", "hawks-work-glider"];
    }
    // land
    if (exp === "new") {
      if (budget === "low") return ["deerc-9309e", "redcat-volcano-epx"];
      if (budget === "mid") return ["redcat-volcano-epx", "arrma-granite"];
      return ["traxxas-slash-4x4", "redcat-volcano-epx"];
    }
    if (budget === "low") return ["losi-micro-b", "redcat-volcano-epx"];
    if (budget === "mid") return ["arrma-granite", "traxxas-slash-4x4"];
    return ["traxxas-slash-4x4", "arrma-granite"];
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  function card(id, heading) {
    var p = products[id];
    if (!p) return null;
    var wrap = el("div", "quiz-card");
    wrap.appendChild(el("span", "quiz-card-kicker", heading));
    wrap.appendChild(el("h3", "", p.name));
    if (p.bestFor) wrap.appendChild(el("p", "", p.bestFor));
    if (p.inBox) {
      wrap.appendChild(el("span", "badge " + (p.inBoxOk ? "badge-ok" : "badge-warn"), p.inBox));
    }
    var actions = el("div", "quiz-actions");
    var buy = el("a", "cta-button", p.cta);
    buy.href = p.url;
    buy.target = "_blank";
    buy.rel = "sponsored nofollow noopener";
    actions.appendChild(buy);
    var more = el("a", "quiz-more", "Read the full guide");
    more.href = p.guide + "#pick-" + id;
    actions.appendChild(more);
    wrap.appendChild(actions);
    return wrap;
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var data = new FormData(form);
    var pair = choose(data.get("where"), data.get("exp"), data.get("budget"));
    out.innerHTML = "";
    var main = card(pair[0], "Our pick for them");
    if (main) out.appendChild(main);
    if (pair[1]) {
      var alt = card(pair[1], "Also worth a look");
      if (alt) out.appendChild(alt);
    }
    out.appendChild(
      el(
        "p",
        "quiz-note",
        "Before you order, check the estimated delivery date and what's included in the box on the listing."
      )
    );
    out.hidden = false;
    out.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });
})();
