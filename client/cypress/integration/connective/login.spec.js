/// <reference types="cypress" />


describe('example to-do app', () => {
  beforeEach(() => {
    // Cypress starts out with a blank slate for each test
    // so we must tell it to visit our website with the `cy.visit()` command.
    // Since we want to visit the same URL at the start of all our tests,
    // we include it in our beforeEach function so that it runs before each test
    cy.visit('https://8080-gray-halibut-x0n7xsmr.ws-eu10.gitpod.io/')
  })

  it('login', () => {
    cy.get('[data-testid="email-input"]').type("coord@example.com")
    cy.get('[data-testid="password-input"]').type("Aa123456789{enter}")
  })
})
