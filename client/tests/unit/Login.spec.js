import Vuetify from "vuetify"
import Vuex from "vuex"
import { mount, createLocalVue } from "@vue/test-utils"
import Login from "@/views/Login.vue"
import flushPromises from "flush-promises"

const localVue = createLocalVue()
localVue.use(Vuex)

describe("Login.vue", () => {
  const email = "user@example.com"
  const password = "password"
  const vuetify = new Vuetify()
  const actions = {
    login: jest.fn(),
  }
  const store = new Vuex.Store({
    modules: {
      auth: {
        namespaced: true,
        actions,
      },
    },
  })

  it("should dispatch login action on submit", async () => {
    const wrapper = mount(Login, {
      vuetify,
      localVue,
      store,
      mocks: {
        $t: key => key,
      },
    })

    let email = "user@example.com"
    let password = "password"
    await wrapper.find('[data-testid="email-input"]').setValue(email)
    await wrapper.find('[data-testid="password-input"]').setValue(password)
    await wrapper.find("form").trigger("submit")
    await flushPromises()
    expect(actions.login).toHaveBeenCalledWith(expect.anything(), {
      email,
      password,
    })
  })

  it("should display an error on invalid credentials response", async () => {
    const wrapper = mount(Login, {
      vuetify,
      store,
      localVue,
      mocks: {
        $t: key => key,
      },
    })

    const loginFailureResponse = {
      response: {
        data: {
          nonFieldErrors: ["Unable to log in with provided credentials."],
        },
      },
    }
    actions.login.mockRejectedValueOnce(loginFailureResponse)
    await wrapper.find('[data-testid="email-input"]').setValue(email)
    await wrapper.find('[data-testid="password-input"]').setValue(password)
    await wrapper.find("form").trigger("submit")
    await flushPromises()
    expect(wrapper.find('[data-testid="modal"]').isVisible()).toBe(true)
    expect(wrapper.vm.popupMsg).toBe("errors.invalidCreds")
  })

  it("should display a generic error on unknown response", async () => {
    const wrapper = mount(Login, {
      vuetify,
      store,
      localVue,
      mocks: {
        $t: key => key,
      },
    })
    expect(wrapper.find('[data-testid="modal"]').isVisible()).toBe(false)

    const loginFailureResponse = {
      response: { data: { oops: "unexpected response from server" } },
    }
    actions.login.mockRejectedValueOnce(loginFailureResponse)
    await wrapper.find('[data-testid="email-input"]').setValue(email)
    await wrapper.find('[data-testid="password-input"]').setValue(password)
    await wrapper.find("form").trigger("submit")
    await flushPromises()
    expect(wrapper.find('[data-testid="modal"]').isVisible()).toBe(true)
    expect(wrapper.vm.popupMsg).toBe("errors.genericError")
  })
})
