/// <reference types="cypress" />

describe("vendor approve/deny event order", () => {
  beforeEach(() => {
    cy.visit(Cypress.env("clientUrl"));
    cy.get('[data-testid="email-input"]').type("test-vendor@example.com");
    cy.get('[data-testid="password-input"]').type("Aa123456789");
    cy.get("form").submit();
    cy.url().should("contain", "dashboard");
    cy.get('[data-testid="events-approve-navbar-tab"]').click();
    cy.url().should("contain", "events-approve");
  });

  it("should approve an event order", () => {
    const pendingApprovalString = "ממתין לאישור מנהל עמותה";
    // const initialPendingApprovalCount = cy.get(
    //   `td:contains(${pendingApprovalString})`
    // ).length;

    cy.get(`td:contains(${pendingApprovalString})`).then(($els) => {
      const initialPendingApprovalCount = $els.length;

      // approve one request
      cy.get(`tr:contains(${pendingApprovalString})`)
        .find('[data-testid="actions-table-action-one"]')
        .first()
        .click();
      cy.get('[data-testid="modal-approve-yes"]').click();

      // check pending approval requests are lower now
      cy.get(`td:contains(${pendingApprovalString})`)
        .its("length")
        .should("be.lt", initialPendingApprovalCount);
    });

    // const newPendingApprovalCount = cy.get(
    //   `td:contains(${pendingApprovalString})`
    // ).length;

    // expect(newPendingApprovalCount).to.have.lengthOf(
    //   initialPendingApprovalCount - 1
    // );
  });

  // it("should reject an event order", () => {});
});
