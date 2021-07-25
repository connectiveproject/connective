/// <reference types="cypress" />

const randomStr = [..."abcdefghijklm"]
  .map((letter, i, arr) => arr[Math.floor(Math.random() * arr.length)])
  .join("");
const randomEmail = `${randomStr}@example.com`;

describe("vendor invite & delete users", () => {
  beforeEach(() => {
    cy.visit(Cypress.env("clientUrl"));
    cy.get('[data-testid="email-input"]').type("test-vendor@example.com");
    cy.get('[data-testid="password-input"]').type("Aa123456789");
    cy.get("form").submit();
    cy.url().should("contain", "dashboard");
    cy.get('[data-testid="user-invite-navbar-btn"]').click();
    cy.url().should("contain", "invite");
  });

  it("should invite an instructor", () => {
    cy.get('[data-testid="invite-instructor-btn"]').click();
    cy.get('[data-testid="instructor-dialog-name-input"]').type("סלים שיידי");
    cy.get('[data-testid="instructor-dialog-email-input"]').type(randomEmail);
    cy.get("form").submit();
    cy.get('[data-testid="invite-instructor-search-field"]').type(
      `${randomEmail}{enter}`
    );
    cy.contains(randomEmail);
    cy.contains("סלים שיידי");

    if (Cypress.env("mailboxUrl")) {
      cy.visit(Cypress.env("mailboxUrl"));
      cy.contains(randomEmail);
    }
  });

  it("should delete an instructor", () => {
    cy.get('[data-testid="invite-instructor-search-field"]').type(
      `${randomEmail}{enter}`
    );
    cy.get(".v-simple-checkbox").should("have.length", 2).last().click();
    cy.get('[data-testid="delete-instructor-btn"]').click();
    cy.contains(randomEmail).should("not.exist");
  });
});
