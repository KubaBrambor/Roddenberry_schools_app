// this script should be run with "pnpm api:generate"
import { exec } from "child_process"
import { promisify } from "util"
import fs from "fs/promises"

const execAsync = promisify(exec)

const API_URL = process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000"
const OUTPUT_PATH = "./types/api.d.ts"
const SPEC_PATH = "./openapi.json"

async function generate() {
    try {
        // Try to fetch latest spec from backend
        console.log(`🔄 Fetching OpenAPI spec from ${API_URL}...`)
        const response = await fetch(`${API_URL}/openapi.json`)
        const spec = await response.json()
        await fs.writeFile(SPEC_PATH, JSON.stringify(spec, null, 2))
        console.log("✅ OpenAPI spec saved")
    } catch (error) {
        console.warn(
            `⚠️  Backend not available, using cached openapi.json, error: ${error}`,
        )
    }

    // Generate types from local spec
    console.log("🔄 Generating TypeScript types...")
    await execAsync(`pnpm openapi-typescript ${SPEC_PATH} -o ${OUTPUT_PATH}`)
    console.log("✅ Types generated successfully!")
}

generate()
