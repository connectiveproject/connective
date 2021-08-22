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
    const originalPendingApprovalCount = cy.get(
      `td:contains(${pendingApprovalString})`
    ).length;
    const actions = cy.get('[data-testid="actions-table-action-one"]');
    for (const action of actions) {
      action.click();
      const approveButtons = cy.$('[data-testid="modal-approve-yes"]');
      if (approveButtons.length) {
        approveButtons[0].click();
      }
      break;
    }

    const newPendingApprovalCount = cy.get(
      `td:contains(${pendingApprovalString})`
    ).length;
    expect(newPendingApprovalCount).to.have.lengthOf(
      originalPendingApprovalCount - 1
    );
  });

  // it("should reject an event order", () => {});
});
