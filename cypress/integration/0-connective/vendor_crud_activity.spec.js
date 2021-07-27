/// <reference types="cypress" />

describe("crud activity", () => {
  beforeEach(() => {
    cy.visit(Cypress.env("clientUrl"));
    cy.get('[data-testid="email-input"]').type("test-vendor@example.com");
    cy.get('[data-testid="password-input"]').type("Aa123456789");
    cy.get("form").submit();
    cy.url().should("contain", "dashboard");
    cy.get('[data-testid="my-programs-navbar-btn"]').click();
    cy.url().should("contain", "my-programs");
  });

  it("should create an activity", () => {
    cy.get('[data-testid="program-create-btn"]').click();
    cy.url().should("contain", "program-creator");

    cy.get('[data-testid="name"]').type("Rapping with the Stars");
    cy.get('[data-testid="description"]').type(
      "I'm Slim Shady, yes, I'm the real Shady"
    );

    cy.get('[data-testid="targetAudience"]').parent().click();
    cy.get(".v-select-list").first().children().first().click();

    cy.get('[data-testid="domain"]').parent().click();
    cy.get(".v-select-list").last().children().first().click();

    cy.get('[data-testid="activityWebsiteUrl"]').type("https://website.com");
    cy.get('[data-testid="activityEmail"]').type("email@example.com");
    cy.get('[data-testid="contactName"]').type("דוד דוד");
    cy.get('[data-testid="phoneNumber"]').type("0521234567");
    cy.get('input[type="file"]').attachFile("testImage.jpg");

    cy.get('[data-testid="save-btn"]').click();
    cy.url().should("contain", "program-media-upload");

    // media upload page
    cy.get('[data-testid="add-media-btn"]').click();
    cy.get('input[type="file"]').attachFile("testImage.jpg");
    cy.get('[data-testid="save-btn"]').click();
    cy.get('[data-testid="add-media-btn"]').click();
    cy.get('[data-testid="media-type-select"]').parent().click();
    cy.get(".v-select-list").last().children().last().click();
    cy.get('input[type="text"]')
      .last()
      .type("https://www.youtube.com/watch?v=dQw4w9WgXcQ");
    cy.get('[data-testid="save-btn"]').click();
    cy.get('[data-testid="finish-btn"]').click();
  });

  it("should update an activity", () => {
    cy.get('[data-testid="info-btn"]').last().click();
    cy.url().should("contain", "detail-program");

    cy.get('[data-testid="input-drawer"]').first().click();
    cy.get('[data-testid="name"]').clear().type("The Slim Shady Program");
    cy.get("form").submit();
    cy.url().should("contain", "my-programs");
    cy.contains("The Slim Shady Program")
  });

  it("should delete an activity", () => {
    cy.get('[data-testid="info-btn"]').last().click();
    cy.url().should("contain", "detail-program");

    cy.get('[data-testid="delete-btn"]').click();
    cy.get('[data-testid="modal-approve-yes"]').click();
    cy.url().should("contain", "my-programs");
  });
});
