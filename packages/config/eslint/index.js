/** @type {import("eslint").Linter.Config[]} */
const config = [
  {
    rules: {
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "no-debugger": "error",
      "prefer-const": "error",
      "no-var": "error",
    },
  },
];

module.exports = config;
