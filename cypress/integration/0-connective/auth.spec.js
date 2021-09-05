/// <reference types="cypress" />

describe("auth", () => {
  beforeEach(() => {
    cy.visit(Cypress.env("clientUrl"))
  })

  it("should login as a coordinator", () => {
    cy.get('[data-testid="email-input"]').type("test-coord@example.com")
    cy.get('[data-testid="password-input"]').type("Aa123456789")
    cy.get("form").submit()
    cy.url().should("contain", "dashboard")
  })

  it("should login as a coordinator for the first time & finish registration", () => {
    cy.get('[data-testid="email-input"]').type("test-signup-coord@example.com")
    cy.get('[data-testid="password-input"]').type("Aa123456789")
    cy.get("form").submit()
    // page 1
    cy.get('[data-testid="name"]').type("דוד לוי")
    cy.get('[data-testid="phone"]').type("0521234567")
    cy.get('[data-testid="form-1"]').submit()
    // page 2
    cy.get('[data-testid="school"]').type("בית ספר שרונים")
    cy.get('[data-testid="school-code"]').type("05646564")
    cy.get('[data-testid="school-city"]').type("תל אביב")
    cy.get('[data-testid="street"]').type("רחוב החבצלת 56")
    cy.get('[data-testid="school-phone"]').type("0521234567")
    cy.get('[data-testid="school-grades"]').parent().click()
    cy.get(".v-select-list").first().children().first().click()
    cy.get('[data-testid="form-2"]').submit()
    cy.get('[data-testid="form-3"]').submit()
    cy.get('[data-testid="modal-button"]').click()
    cy.url().should("contain", "dashboard")
  })

  it("should send password recovery email to consumer", () => {
    const email = "test-consumer-10@example.com"
    cy.get('[data-testid="forgot-pass-btn"]').click()
    cy.get('[data-testid="email-input"]').type(email)
    cy.get("#recaptcha-anchor > div.recaptcha-checkbox-border").click()
    cy.wait(500) // eslint-disable-line
    cy.get("form").submit()
    cy.url().should("contain", "login")
    if (Cypress.env("mailboxUrl")) {
      cy.visit(Cypress.env("mailboxUrl"))
      cy.contains(email)
    }
  })
})
