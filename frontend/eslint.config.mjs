// @ts-check
import withNuxt from "./.nuxt/eslint.config.mjs";
import eslintConfigPrettier from "eslint-config-prettier/flat";

export default withNuxt({
    ignores: [
        "**/node_modules/**",
        "**/.nuxt/**",
        "**/.output/**",
        "**/dist/**",
        "**/coverage/**",
        "**/.husky/**",
        "**/.vscode/**",
        "**/.idea/**",
        "**/.DS_Store",
    ],
    rules: {
        "no-else-return": 2,
    },
}).append(eslintConfigPrettier);
