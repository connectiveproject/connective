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
    cy.wait(1000);
  });

  it("should approve an event order", () => {
    const pendingApprovalString = "ממתין לאישור מנהל עמותה";
    cy.get(`td:contains(${pendingApprovalString})`).then(($elems) => {
      const initialPendingApprovalCount = $elems.length;
      cy.get(`tr:contains(${pendingApprovalString})`)
        .find('[data-testid="actions-table-action-one"]')
        .first()
        .click();
      cy.get('[data-testid="modal-approve-yes"]').click();
      cy.wait(500);

      cy.get(`td:contains(${pendingApprovalString})`)
        .its("length")
        .should("be.lt", initialPendingApprovalCount);
    });
  });

  it("should reject an event order", () => {
    const rejectionString = "זמנים אלה אינם מתאימים לביצוע הפעילות";
    const pendingApprovalString = "ממתין לאישור מנהל עמותה";
    cy.get(`td:contains(${pendingApprovalString})`).then(($elems) => {
      const initialPendingApprovalCount = $elems.length;
      cy.get(`tr:contains(${pendingApprovalString})`)
        .find('[data-testid="actions-table-action-two"]')
        .first()
        .click();
      cy.get('[data-testid="form-dialog"')
        .get("input")
        .type(`${rejectionString}{enter}`);
      cy.wait(500);

      cy.get(`td:contains(${pendingApprovalString})`)
        .its("length")
        .should("be.lt", initialPendingApprovalCount);
    });
    cy.contains(rejectionString);
  });
});
