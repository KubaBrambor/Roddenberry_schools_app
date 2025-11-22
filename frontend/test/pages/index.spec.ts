import { mount } from "@vue/test-utils"
import { ref } from "vue"
import IndexPage from "../../pages/index.vue"

// Mock the composable used by the page to avoid hitting real network/Nuxt runtime
vi.mock("../../composables/useApi", () => {
    return {
        useApi: () => {
            return {
                data: ref({ message: "Hello from test" }),
                error: ref(null),
                status: ref("success"),
            }
        },
    }
})

describe("pages/index.vue", () => {
    it("renders header and backend response from mocked composable", async () => {
        const wrapper = mount(IndexPage)
        expect(wrapper.find("h1").text()).toBe("Test połączenia z backendem")
        expect(wrapper.text()).toContain(
            "Odpowiedź z backendu: Hello from test",
        )
    })
})
