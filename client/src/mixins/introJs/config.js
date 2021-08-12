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
  VendorDashboard: [
    {
      title: i18n.t("introjs.welcome!"),
      intro: i18n.t(
        "introjs.welcomeToConnective!InThePlatformYouWouldBeAbleToIntroduceYourProgramsCollaborateWithSchoolsEtc"
      ),
    },
    {
      title: i18n.t("introjs.avatar"),
      selector: "navbar-account-menu",
      intro: i18n.t(
        "intro.js.byClickingTheAvatarYouCanPerformUserActionsAndGetExplanationsForTheDifferentPages"
      ),
    },
    {
      title: i18n.t("introjs.navigation"),
      selector: "navigation",
      intro: i18n.t("בלחיצה ניתן לנווט לעמודים השונים בממשק."),
    },
  ],
  CoordinatorDashboard: [
    {
      title: i18n.t("introjs.welcome!"),
      intro: i18n.t(
        "introjs.welcomeToConnective!InThePlatformYouWouldBeAbleToConsumeNewActivitiesToYourSchoolMonitorGroupsAndEventsEtc"
      ),
    },
    {
      title: i18n.t("introjs.avatar"),
      selector: "navbar-account-menu",
      intro: i18n.t(
        "intro.js.byClickingTheAvatarYouCanPerformUserActionsAndGetExplanationsForTheDifferentPages"
      ),
    },
    {
      title: i18n.t("introjs.navigation"),
      selector: "navigation",
      intro: i18n.t("introjs.clickToNavigateToTheDifferentPages"),
    },
  ],
  StudentDashboard: [
    {
      title: i18n.t("introjs.welcome!"),
      intro: i18n.t(
        "introjs.welcomeToConnective!InThePlatformYouWouldBeAbleToJoinTheActiveProgramsInYourSchoolViewUpdatesAndNewsEtc"
      ),
    },
    {
      title: i18n.t("introjs.avatar"),
      selector: "navbar-account-menu",
      intro: i18n.t(
        "intro.js.byClickingTheAvatarYouCanPerformUserActionsAndGetExplanationsForTheDifferentPages"
      ),
    },
    {
      title: i18n.t("introjs.navigation"),
      selector: "navigation",
      intro: i18n.t("introjs.clickToNavigateToTheDifferentPages"),
    },
  ],
  InstructorDashboard: [
    {
      title: i18n.t("introjs.welcome!"),
      intro: i18n.t(
        "introjs.welcomeToConnective!InThePlatformYouWouldBeAbleToKeepTrackOfTheStudentsStatusSummarizeEventsEtc"
      ),
    },
    {
      title: i18n.t("introjs.avatar"),
      selector: "navbar-account-menu",
      intro: i18n.t(
        "intro.js.byClickingTheAvatarYouCanPerformUserActionsAndGetExplanationsForTheDifferentPages"
      ),
    },
    {
      title: i18n.t("introjs.navigation"),
      selector: "navigation",
      intro: i18n.t("introjs.clickToNavigateToTheDifferentPages"),
    },
  ],
  VendorProgramList: [
    {
      title: i18n.t("introjs.myPrograms"),
      intro: i18n.t(
        "introjs.inThisPageYouCanViewTheExistingProgramsAndAddNewOnes"
      ),
    },
    {
      title: i18n.t("introjs.add"),
      selector: "program-create-btn",
      intro: i18n.t("introjs.clickTheButtonToAddNewPrograms"),
    },
  ],
  VendorEventsApprove: [
    {
      title: i18n.t("introjs.eventsStatus"),
      selector: "actions-table",
      intro: i18n.t(
        "בטבלה ניתן לראות אילו בתי ספר ביקשו להטמיע את התוכניות בתוכנית לימודיהם. ניתן לאשר ולדחות את הבקשה באמצעות הכפתורים בצד הטבלה."
      ),
    },
  ],
  SchoolInviteWrapper: [
    {
      title: i18n.t("introjs.inviteUsers"),
      intro: i18n.t(
        "introjs.inThisPageYouCanInviteAndDeleteUsersForThePlatform"
      ),
    },
    {
      title: i18n.t("introjs.inviteUsers"),
      selector: "tabs",
      intro: i18n.t("introjs.youCanInviteStudentsAndStaffSeperately"),
    },
    {
      title: i18n.t("introjs.inviteUsers"),
      selector: "table-actions",
      intro: i18n.t(
        "introjs.clickTheInviteButtonToInviteNewUser-TheUserWillReceiveInviteThroughTheSpecifiedEmail"
      ),
    },
    {
      title: i18n.t("introjs.inviteUsers"),
      selector: "table-actions",
      intro: i18n.t(
        "introjs.additionalActionsAreAvailable-selectAndDeleteUsersInviteViaExcelUpload-WeRecommendExportingExcelFileFillingItAndUpload"
      ),
    },
  ],
  OrganizationInviteWrapper: [
    {
      title: i18n.t("introjs.inviteUsers"),
      intro: i18n.t(
        "introjs.inThisPageYouCanInviteAndDeleteUsersForThePlatform"
      ),
    },
    {
      title: i18n.t("introjs.inviteUsers"),
      selector: "tabs",
      intro: i18n.t("introjs.youCanInviteInstructorsAndVendorsSeperately"),
    },
    {
      title: i18n.t("introjs.inviteUsers"),
      selector: "table-actions",
      intro: i18n.t(
        "introjs.clickTheInviteButtonToInviteNewUser-TheUserWillReceiveInviteThroughTheSpecifiedEmail"
      ),
    },
    {
      title: i18n.t("introjs.inviteUsers"),
      selector: "table-actions",
      intro: i18n.t(
        "introjs.additionalActionsAreAvailable-selectAndDeleteUsersInviteViaExcelUpload-WeRecommendExportingExcelFileFillingItAndUpload"
      ),
    },
  ],
  ConsumerProgramsExplorer: [
    {
      title: i18n.t("introjs.programExplorer"),
      intro: i18n.t(
        "introjs.inThisPageYouCanBrowseTheProgramCatalogAndChooseAProgramToJoin"
      ),
    },
    {
      title: i18n.t("introjs.search"),
      selector: "search",
      intro: i18n.t("introjs.searchUsingKeywordsForExampleProgramName"),
    },
    {
      title: i18n.t("introjs.filter"),
      selector: "advanced-search",
      intro: i18n.t("introjs.smartFilteringIsAvailable"),
    },
    {
      title: i18n.t("introjs.choosingProgram"),
      intro: i18n.t(
        "introjs.afterBrowsingTheCatalogYouCanChooseAProgramToJoin-requestWillBeSentToTheSchoolStaffAndYouWillBeAssignedToGroupAfterApproval"
      ),
    },
  ],
  ProgramsExplorer: [
    {
      title: i18n.t("introjs.programExplorer"),
      intro: i18n.t(
        "introjs.inThisPageYouCanBrowseTheProgramCatalogAndChooseProgramsForYourSchool"
      ),
    },
    {
      title: i18n.t("introjs.search"),
      selector: "search",
      intro: i18n.t("introjs.searchUsingKeywordsForExampleProgramName"),
    },
    {
      title: i18n.t("introjs.filter"),
      selector: "advanced-search",
      intro: i18n.t("introjs.smartFilteringIsAvailable"),
    },
    {
      title: i18n.t("introjs.choosingProgram"),
      intro: i18n.t(
        "introjs.afterBrowsingTheCatalogYouCanChooseAProgramToJoinTo-RequestWillBeSentToThePlatformAdministrators"
      ),
    },
  ],
  ConsumerProfile: [
    {
      title: i18n.t("introjs.myProfile"),
      intro: i18n.t(
        "introjs.inThisPageYouCanViewYourProfileAndEditTheAvatarImage"
      ),
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
      title: i18n.t("המפגשים שלי"),
      intro: i18n.t(
        "בעמוד זה ניתן לצפות במפגשים השבועיים של הקבוצות אליהן נרשמת."
      ),
    },
    {
      title: i18n.t("המפגשים שלי"),
      intro: i18n.t(
        "ניתן להתבונן במפגשים לפי תאריך, כאשר בלחיצה על מפגש ספציפי, ייפתח פירוט."
      ),
      selector: "events-calendar",
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
      intro: i18n.t(
        "בחלק זה ניתן לצפות בקבוצות הפועלות בבית הספר. תחת כל פעילות עשויות להתקיים מספר קבוצות במקביל. לדוגמה - תוכנית מצויינות עם קבוצות גיל שונות."
      ),
    },
    {
      title: i18n.t("הקבוצות שלי"),
      intro: i18n.t(
        "בלחיצה על כפתור זה ניתן לייצר קבוצות חדשות תחת פעילויות שאושרו לבית הספר."
      ),
      selector: "add-btn",
    },
  ],
  MyEvents: [
    {
      title: i18n.t("המפגשים שלי"),
      intro: i18n.t("בעמוד זה ניתן לצפות במפגשים השבועיים של הקבוצות השונות."),
    },
    {
      title: i18n.t("המפגשים שלי"),
      intro: i18n.t(
        "ניתן להתבונן במפגשים לפי תאריך, כאשר בלחיצה על מפגש ספציפי, ייפתח פירוט."
      ),
      selector: "events-calendar",
    },
    {
      title: i18n.t("המפגשים שלי"),
      intro: i18n.t(
        "בלחיצה על כפתור זה ניתן להתבונן בסטטוס בקשות המפגשים, כמו גם ליצור בקשה חדשה."
      ),
      selector: "events-table-button",
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
        "בחלק זה ניתן לייצר פוסט/פרסום פומבי בו יוכלו תלמידים וסגל לצפות. חלק זה מגביר את זיקת התלמיד לפעילות. ניתן להעלות תמונות, להוסיף תיאור ועוד."
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
  VendorGroupsTable: [
    {
      title: i18n.t("myActivity.myGroups"),
      intro: i18n.t(
        "בעמוד זה ניתן לצפות בכלל הקבוצות שבבעלות העמותה ולשבץ מדריכים בהתאם"
      ),
    },
    {
      title: i18n.t("myActivity.myGroups"),
      selector: "actions-table-icon-one",
      intro: i18n.t("בלחיצה כאן ניתן לשבץ מדריך לקבוצה"),
    },
  ],
}
