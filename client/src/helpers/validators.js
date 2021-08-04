import moment from "moment"
import i18n from "../plugins/i18n"
import {
  required,
  email,
  size,
  max,
  numeric,
  digits,
} from "vee-validate/dist/rules"
import { extend } from "vee-validate"
import {
  PASSWORD_REGEX_PATTERN,
  ISRAELI_PHONE_REGEX_PATTERN,
  WEBSITE_REGEX_PATTERN,
  YOUTUBE_URL_REGEX_PATTERN,
} from "./constants/constants"

extend("required", {
  ...required,
  message: i18n.tc("errors.requiredField"),
})

extend("email", {
  ...email,
  message: i18n.tc("errors.invalidEmail"),
})

extend("numeric", {
  ...numeric,
  message: i18n.tc("errors.NumbersOnlyField"),
})

extend("strongPass", {
  message: i18n.tc("errors.strongPassHint"),
  validate: value => {
    let strongRegex = new RegExp(PASSWORD_REGEX_PATTERN)
    return strongRegex.test(value)
  },
})

extend("passConfirm", {
  params: ["target"],
  validate(value, { target }) {
    return value === target
  },
  message: i18n.tc("errors.passwordsMismatch"),
})

extend("phoneNumberIsrael", {
  message: i18n.tc("errors.invalidPhoneNumber"),
  validate: value => {
    let strongRegex = new RegExp(ISRAELI_PHONE_REGEX_PATTERN)
    return strongRegex.test(value)
  },
})

extend("website", {
  message: i18n.tc("errors.invalidWebsiteAddress"),
  validate: value => {
    const regex = new RegExp(WEBSITE_REGEX_PATTERN, "i")
    return regex.test(value)
  },
})

extend("size", {
  ...size,
  message: i18n.tc("errors.fileSizeLimitExceeded"),
})

extend("max", {
  ...max,
  message: i18n.tc("errors.maxLengthExceeded"),
})

extend("digits", {
  ...digits,
  message: i18n.tc("errors.incorrectNumberOfDigits"),
})

extend("youtubeUrl", {
  message: i18n.tc("errors.invalidYoutubeUrl"),
  validate: value => {
    const regex = new RegExp(YOUTUBE_URL_REGEX_PATTERN, "i")
    return regex.test(value)
  },
})

extend("afterStartDate", {
  // should be attached to end-time
  // check if end-time + end-date is after start-time + start-date
  params: ["startDate", "startTime", "endDate"],
  validate(endTime, { startDate, startTime, endDate }) {
    if (!endTime || !startDate || !startTime || !endDate) {
      return true
    }
    const startDateObj = moment(`${startDate}T${startTime}`)
    const endDateObj = moment(`${endDate}T${endTime}`)
    return endDateObj.isAfter(startDateObj)
  },
  message: i18n.tc("errors.endTimeShouldBeLaterThanStartTime"),
})
