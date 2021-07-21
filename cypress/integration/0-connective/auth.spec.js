/// <reference types="cypress" />

describe("auth", () => {
  beforeEach(() => {
    cy.visit(Cypress.env("clientUrl"))
  })

  it("should login as a consumer", () => {
    cy.get('[data-testid="email-input"]').type("test-coord@example.com")
    cy.get('[data-testid="password-input"]').type("Aa123456789")
    cy.get("form").submit()
    cy.url().should("contain", "dashboard")
  })

  it("should login as a coord for the first time & finish registration", () => {
    cy.get('[data-testid="email-input"]').type("test-coord@example.com")
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
    cy.get('[data-testid="school-zip-code"]').type("0522131")
    cy.get('[data-testid="school-phone"]').type("0521234567")
    cy.get('[data-testid="school-description"]').type("ביס יסודי שרונים")
    cy.get('[data-testid="school-website"]').type("https://example.com")
    cy.get('[data-testid="school-grades"]').parent().click()
    cy.get(".v-select-list").first().children().first().click()
    cy.get('[data-testid="form-2"]').submit()
    cy.get('[data-testid="form-3"]').submit()
    cy.get('[data-testid="modal-button"]').click()
    cy.url().should("contain", "dashboard")
  })
})
