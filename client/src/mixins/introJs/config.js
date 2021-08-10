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
  VendorProgramList: [
    {
      title: i18n.t("התוכניות שלי"),
      intro: i18n.t(
        "בעמוד זה ניתן לצפות בתוכניות הקיימות תחתיכם ולהוסיף תוכניות חדשות"
      ),
    },
    {
      title: i18n.t("הוספה"),
      selector: "program-create-btn",
      intro: i18n.t("בלחיצה על כפתור זה ניתן להוסיף תוכניות חדשות"),
    },
  ],
  VendorEventsApprove: [
    {
      title: i18n.t("סטטוס מפגשים"),
      selector: "actions-table",
      intro: i18n.t(
        "בטבלה ניתן לראות אילו בתי ספר ביקשו להטמיע את התוכניות בתוכנית לימודיהם. ניתן לאשר ולדחות את הבקשה באמצעות הכפתורים בצד הטבלה."
      ),
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
  ConsumerProgramsExplorer: [
    {
      title: i18n.t("חוקר התוכניות"),
      intro: i18n.t(
        "בעמוד זה ניתן לעיין בקטלוג התוכניות ולבחור תוכנית אליה תרצו להשתבץ."
      ),
    },
    {
      title: "חיפוש",
      selector: "search",
      intro: i18n.t("ניתן לחפש על פי מילות מפתח. לדוגמה - לפי שם התוכנית"),
    },
    {
      title: "סינון",
      selector: "advanced-search",
      intro: i18n.t("ניתן לבצע סינון חכם"),
    },
    {
      title: i18n.t("בחירת תוכנית"),
      intro: i18n.t(
        "לאחר עיון בתוכניות, ניתן לבחור תוכנית להצטרפות. הבקשה תמתין סגל בית הספר ולאחריה יתבצע שיבוץ לקבוצה"
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
      title: "חיפוש",
      selector: "search",
      intro: i18n.t("ניתן לחפש על פי מילות מפתח. לדוגמה - לפי שם התוכנית"),
    },
    {
      title: "סינון",
      selector: "advanced-search",
      intro: i18n.t("ניתן לבצע סינון חכם"),
    },
    {
      title: i18n.t("בחירת תוכנית"),
      intro: i18n.t(
        "לאחר עיון בתוכניות, ניתן לבחור תוכנית להצטרפות, קרי להטמעה בבית הספר. הבקשה תמתין לאישור מנהל מערכת"
      ),
    },
  ],
  ConsumerProfile: [
    {
      title: i18n.t("הפרופיל שלי"),
      intro: i18n.t("בעמוד זה ניתן לצפות בפרטי הפרופיל ולערוך את תמונת האווטר"),
    },
  ],
  ConsumerMyGroups: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  ConsumerMyEvents: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  ConsumerPendingEventsFeedback: [
    {
      title: i18n.t("מישוב מפגשים"),
      intro: i18n.t(
        "בעמוד זה ניתן למלא פידבק על הפעילויות השונות על מנת שנוכל להשתפר יחדיו"
      ),
      selector: "click-list",
    },
  ],
  ConsumerEventFeedback: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  CoordinatorProfile: [
    {
      title: i18n.t("הפרופיל שלי"),
      intro: i18n.t("בעמוד זה ניתן לערוך את פרטי הפרופיל ואת תמונת האווטר"),
    },
  ],
  SchoolDetails: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  ProgramModal: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  MyGroups: [
    {
      title: i18n.t("הקבוצות שלי"),
      intro: i18n.t("בחלק זה ניתן לצפות בקבוצות הפועלות בבית הספר. תחת כל פעילות עשויות להתקיים מספר קבוצות במקביל. לדוגמה - תוכנית מצויינות עם קבוצות גיל שונות."),
    },
    {
      title: i18n.t("הקבוצות שלי"),
      intro: i18n.t("בלחיצה על כפתור זה ניתן לייצר קבוצות חדשות תחת פעילויות שאושרו לבית הספר."),
      selector: "add-btn",
    },
  ],
  MyEvents: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  ConsumerList: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  CoordinatorStatistics: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  GroupDetail: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  CoordinatorEventOrderStatus: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  CoordinatorEventCreator: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  GroupEditor: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  CreateGroup: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  AssignGroupConsumers: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  InstructorProfile: [
    {
      title: i18n.t("הפרופיל שלי"),
      intro: i18n.t("בעמוד זה ניתן לצפות בפרטי הפרופיל ולערוך את תמונת האווטר"),
    },
  ],
  InstructorUnsummarizedEvents: [
    {
      title: i18n.t("סיכום מפגשים"),
      intro: i18n.t(
        "בעמוד זה ניתן לבצע סיכומי מפגשים, מילוי נוכחות, כתיבת הערות ופרסום פוסטים פומביים"
      ),
      selector: "click-list",
    },
  ],
  InstructorEventSummary: [
    {
      title: i18n.t("סיכום מפגש"),
      intro: i18n.t("כאן ניתן לסכם מפגש עבר"),
    },
    {
      title: i18n.t("חסוי"),
      selector: "confidential",
      intro: i18n.t(
        "חלק זה הוא החלק החסוי שאינו משוקף לתלמידים. ניתן למלא נוכחות, אירועים חריגים ומרכזיים שקרו ועוד."
      ),
    },
    {
      title: i18n.t("פומבי"),
      selector: "public",
      intro: i18n.t(
        "בחלק זה ניתן לייצר פוסט/פרסום פומבי בו יוכלו תלמידים וסגל לצפות. חלק זה מגביר את זיקת התלמיד לפעילות. ניתן להעלות תמונות, סרטונים ועוד."
      ),
    },
  ],
  EventFeedView: [
    {
      title: i18n.t("הפיד שלי"),
      intro: i18n.t(
        "בעמוד זה ניתן לצפות בפוסטים ובפרסומים מן הפעילויות השונות"
      ),
    },
  ],
  VendorProfile: [
    {
      title: i18n.t("הפרופיל שלי"),
      intro: i18n.t("בעמוד זה ניתן לערוך את פרטי הפרופיל ואת תמונת האווטר"),
    },
  ],
  VendorDetailProgram: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  VendorProgramCreator: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
  VendorProgramMediaUpload: [
    {
      title: i18n.t("errors.oops"),
      intro: i18n.t("errors.noAvailableExplanation"),
    },
  ],
}
