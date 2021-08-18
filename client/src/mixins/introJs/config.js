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
        "introjs.byClickingTheAvatarYouCanPerformUserActionsAndGetExplanationsForTheDifferentPages"
      ),
      preStepAction() {
        document.querySelector(`[introjs="navbar-account-menu"]`).children[0].click()
      },
    },
    {
      title: i18n.t("introjs.navigation"),
      selector: "navigation",
      intro: i18n.t("introjs.clickToNavigateToTheDifferentPages"),
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
        "introjs.byClickingTheAvatarYouCanPerformUserActionsAndGetExplanationsForTheDifferentPages"
      ),
      preStepAction() {
        document.querySelector(`[introjs="navbar-account-menu"]`).children[0].click()
      },
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
        "introjs.byClickingTheAvatarYouCanPerformUserActionsAndGetExplanationsForTheDifferentPages"
      ),
      preStepAction() {
        document.querySelector(`[introjs="navbar-account-menu"]`).children[0].click()
      },
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
        "introjs.byClickingTheAvatarYouCanPerformUserActionsAndGetExplanationsForTheDifferentPages"
      ),
      preStepAction() {
        document.querySelector(`[introjs="navbar-account-menu"]`).children[0].click()
      },
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
      title: i18n.t("introjs.requestsForEvents"),
      selector: "actions-table",
      intro: i18n.t(
        "introjs.inThisTableYouCanSeeWhichSchoolsRequestedYourPrograms-YouMayAcceptAndRejectTheRequestsUsingTheTableSideButtons"
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
      title: i18n.t("introjs.programCatalog"),
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
      title: i18n.t("introjs.programCatalog"),
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
      title: i18n.t("introjs.myEvents"),
      intro: i18n.t(
        "introjs.inThisPageYouCanViewTheWeeklyEventsOfTheGroupsYouRegisteredTo"
      ),
    },
    {
      title: i18n.t("introjs.myEvents"),
      intro: i18n.t(
        "introjs.youCanViewTheEventsByDate-YouCanAlsoViewAdditionalInfoByClickingOnEvent"
      ),
      selector: "events-calendar",
    },
  ],
  ConsumerPendingEventsFeedback: [
    {
      title: i18n.t("introjs.eventsFeedback"),
      intro: i18n.t(
        "introjs.inThisPageYouCanFillFeedbackOnTheDifferentActivitiesSoWeCanImproveTogether"
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
      title: i18n.t("introjs.myProfile"),
      intro: i18n.t(
        "introjs.inThisPageYouCanEditYourProfileInfoAndAvatarImage"
      ),
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
      title: i18n.t("introjs.myGroups"),
      intro: i18n.t(
        "introjs.inThisSectionYouCanViewTheRunningGroupsInYourSchool-EachProgramMayContainMoreThanOneGroup-forExampleExcellencyProgramWithSeveralAgeGroups"
      ),
    },
    {
      title: i18n.t("introjs.myGroups"),
      intro: i18n.t(
        "introjs.clickThisButtonToCreateNewGroupsForApprovedPrograms"
      ),
      selector: "add-btn",
    },
  ],
  MyEvents: [
    {
      title: i18n.t("introjs.myEvents"),
      intro: i18n.t(
        "introjs.inThisPageYouCanViewWeeklyEventsOfTheDifferentGroups"
      ),
    },
    {
      title: i18n.t("introjs.myEvents"),
      intro: i18n.t(
        "introjs.youCanViewTheEventsByDate-YouCanAlsoViewAdditionalInfoByClickingOnEvent"
      ),
      selector: "events-calendar",
    },
    {
      title: i18n.t("introjs.myEvents"),
      intro: i18n.t(
        "introjs.clickThisButtonToViewTheEventsRequestsStatusAndCreateNewRequests"
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
      title: i18n.t("introjs.myProfile"),
      intro: i18n.t(
        "introjs.inThisPageYouCanViewYourProfileAndEditTheAvatarImage"
      ),
    },
  ],
  InstructorUnsummarizedEvents: [
    {
      title: i18n.t("introjs.eventsSummary"),
      intro: i18n.t(
        "introjs.inThisPageYouMaySummarizeEventsFillInAttendanceWriteEventNotesAndPostPublicPosts"
      ),
      selector: "click-list",
    },
  ],
  InstructorEventSummary: [
    {
      title: i18n.t("introjs.eventSummary"),
      intro: i18n.t("introjs.hereYouMaySummarizeAnEvent"),
    },
    {
      title: i18n.t("introjs.confidential"),
      selector: "confidential",
      intro: i18n.t(
        "introjs.thisSectionIsConfidentialAndStudentsCanNotSeeIt-YouCanFillInAttendanceUnusualIssuesEtc"
      ),
    },
    {
      title: i18n.t("introjs.public"),
      selector: "public",
      intro: i18n.t(
        "introjs.hereYouCanCreateAPublicPostWhichWillBeAvailableForStudentsAndStaff-ThisPartEnhancesStudentsEngagement-YouMayUploadImagesAddDescriptionEtc"
      ),
    },
  ],
  EventFeedView: [
    {
      title: i18n.t("introjs.myFeed"),
      intro: i18n.t("introjs.hereYouMayViewPostsFromTheDifferentActivities"),
    },
  ],
  VendorProfile: [
    {
      title: i18n.t("introjs.myProfile"),
      intro: i18n.t(
        "introjs.inThisPageYouCanEditYourProfileInfoAndAvatarImage"
      ),
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
      title: i18n.t("introjs.myGroups"),
      intro: i18n.t(
        "introjs.hereYouMayViewAllTheGroupsAndAssignInstructorsAccordingly"
      ),
    },
    {
      title: i18n.t("introjs.myGroups"),
      selector: "actions-table-icon-one",
      intro: i18n.t(
        "introjs.clickTheButtonOnTheSideOfEachTableRowToAssignInstructorToTheGroup"
      ),
    },
  ],
}
