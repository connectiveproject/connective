import i18n from "../plugins/i18n"
import { required, email, size, numeric, digits } from "vee-validate/dist/rules"
import { extend } from "vee-validate"
import {
  passwordRegexPattern,
  israeliPhoneRegexPattern,
  websiteRegexPattern,
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
    let strongRegex = new RegExp(passwordRegexPattern)
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
    let strongRegex = new RegExp(israeliPhoneRegexPattern)
    return strongRegex.test(value)
  },
})

extend("website", {
  message: i18n.tc("errors.invalidWebsiteAddress"),
  validate: value => {
    const regex = new RegExp(websiteRegexPattern)
    return regex.test(value)
  },
})

extend("size", {
  ...size,
  message: i18n.tc("errors.fileSizeLimitExceeded"),
})

extend("digits", {
  ...digits,
  message: i18n.tc("errors.incorrectNumberOfDigits"),
})
