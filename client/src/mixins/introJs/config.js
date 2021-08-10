import i18n from "../../plugins/i18n"

export const buttonLabels = {
  nextLabel: i18n.t("userActions.next"),
  prevLabel: i18n.t("userActions.back"),
  doneLabel: i18n.t("userActions.finish"),
}
export const config = {
  noIntroMsg: [
    {
      title: "Sorry!",
      intro: "No helper here.... 👋",
    },
  ],
  SchoolInviteWrapper: [
    {
      title: i18n.t("הזמנת משתמשים"),
      intro: i18n.t("בעמוד זה ניתן להזמין ולמחוק משתמשים מן הפלטפורמה"),
    },
    {
      title: i18n.t("הזמנת משתמשים"),
      selector: "tabs",
      intro: i18n.t("ניתן לבחור בתצוגת תלמידים ובתצוגת אנשי סגל."),
    },
    {
      title: "הזמנה",
      selector: "table-actions",
      intro: i18n.t(
        "לחצו על כפתור ההזמנה על מנת להזמין משתמש חדש. המשתמש יקבל הזמנה למערכת דרך תיבת המייל שצויינה."
      ),
    },
    {
      title: "מחיקה והעלאה",
      selector: "table-actions",
      intro: i18n.t(
        "ניתן לבצע פעולות נוספות - מחיקת משתמשים (לאחר סימונם בטבלה) והזמנת רשימת משתמשים באמצעות העלאת קובץ אקסל. נמליץ לייצא קובץ לדוגמה ולמלאו."
      ),
    },
  ],
  OrganizationInviteWrapper: [
    {
      title: i18n.t("הזמנת משתמשים"),
      intro: i18n.t("בעמוד זה ניתן להזמין ולמחוק משתמשים מן הפלטפורמה"),
    },
    {
      title: i18n.t("הזמנת משתמשים"),
      selector: "tabs",
      intro: i18n.t("ניתן לבחור בתצוגת תלמידים ובתצוגת אנשי סגל."),
    },
    {
      title: "הזמנה",
      selector: "table-actions",
      intro: i18n.t(
        "לחצו על כפתור ההזמנה על מנת להזמין משתמש חדש. המשתמש יקבל הזמנה למערכת דרך תיבת המייל שצויינה."
      ),
    },
    {
      title: "מחיקה והעלאה",
      selector: "table-actions",
      intro: i18n.t(
        "ניתן לבצע פעולות נוספות - מחיקת משתמשים (לאחר סימונם בטבלה) והזמנת רשימת משתמשים באמצעות העלאת קובץ אקסל. נמליץ לייצא קובץ לדוגמה ולמלאו."
      ),
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
      selector: "advanced-search",
      intro: i18n.t("ניתן לבצע סינון חכם"),
    },
    {
      title: "חיפוש",
      selector: "search",
      intro: i18n.t("ניתן לחפש על פי מילות מפתח. לדוגמה - לפי שם התוכנית"),
    },
    {
      title: i18n.t("בחירת תוכנית"),
      intro: i18n.t(
        "לאחר עיון בתוכניות, ניתן לבחור תוכנית להצטרפות, קרי להטמעה בבית הספר. הבקשה תמתין לאישור מנהל מערכת"
      ),
    },
  ],
}
