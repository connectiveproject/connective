import moment from "moment"
import i18n from "@/plugins/i18n"
import {
  required,
  email,
  size,
  max,
  numeric,
  digits,
} from "vee-validate/dist/rules"
import { extend, configure } from "vee-validate"
import {
  PASSWORD_REGEX_PATTERN,
  ISRAELI_PHONE_REGEX_PATTERN,
  WEBSITE_REGEX_PATTERN,
  YOUTUBE_URL_REGEX_PATTERN,
  HEBREW_REGEX_PATTERN,
  ARABIC_REGEX_PATTERN,
} from "./constants/constants"


configure({
  defaultMessage(field, values) {
    return i18n.t(`validation.${values._rule_}`, values)
  }
})

extend("required", required)
extend("email", email)
extend("numeric", numeric)
extend("size", size)
extend("max", max)
extend("digits", digits)

extend("strongPass", {
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
})

extend("phoneNumberIsrael", {
  validate: value => {
    let strongRegex = new RegExp(ISRAELI_PHONE_REGEX_PATTERN)
    return strongRegex.test(value)
  },
})

extend("website", {
  validate: value => {
    const regex = new RegExp(WEBSITE_REGEX_PATTERN, "i")
    return regex.test(value)
  },
})

extend("youtubeUrl", {
  validate: value => {
    const regex = new RegExp(YOUTUBE_URL_REGEX_PATTERN, "i")
    return regex.test(value)
  },
})

extend("afterStartTime", {
  // should be attached to end-time
  // check if end time is greater than start time
  params: ["startTime"],
  validate(endTime, { startTime }) {
    if (!startTime) return true
    const startTimeObj = moment(startTime, "HH:mm")
    const endTimeObj = moment(endTime, "HH:mm")
    return endTimeObj.isAfter(startTimeObj)
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
})

extend("maxDaysDelta", {
  // this date come after another date by maximum number of days
  params: ["date2", "daysDelta"],
  validate(date, { date2, daysDelta }) {
    const dateObj = moment(date)
    const date2Obj = moment(date2)
    return dateObj.diff(date2Obj, "days") <= daysDelta
  },
})

extend("noHebrew", {
  validate: value => {
    let hebrewRegex = new RegExp(HEBREW_REGEX_PATTERN)
    return !hebrewRegex.test(value)
  },
})

extend("noArabic", {
  validate: value => {
    let arabicRegex = new RegExp(ARABIC_REGEX_PATTERN)
    return !arabicRegex.test(value)
  },
})
