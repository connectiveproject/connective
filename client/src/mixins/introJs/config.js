import i18n from "../../plugins/i18n"

export default {
  noIntroMsg: [
    {
      title: "Sorry!",
      intro: "No helper here.... 👋",
    },
  ],
  ProgramsExplorer: [
    {
      title: i18n.t("חוקר התוכניות"),
      intro: i18n.t(
        "בעמוד זה ניתן לעיין בקטלוג התוכניות ולבחור תוכנית להטמעה בבית הספר"
      ),
    },
    {
      title: "סינון",
      element: document.querySelector(".introjs-advanced-search"),
      intro: i18n.t("ניתן לבצע סינון חכם"),
    },
    {
      title: "חיפוש",
      element: document.querySelector(".introjs-search"),
      intro: i18n.t("ניתן לחפש על פי מילות מפתח. לדוגמה - לפי שם התוכנית"),
    },
  ],
}
