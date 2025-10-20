# PROMPT FOR CONTINUING RECIPE HTML CREATION

I need you to continue creating recipe HTMLs from the Mastering Pasta cookbook. Follow these exact 4 steps for each recipe:

## STEP 1: Find the Next Recipe
- Read `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta/recipe-inventory.md`
- Find the NEXT missing recipe (the first one with `- [ ]` checkbox)
- Note the recipe name and page number

## STEP 2: Create the HTML File
**CRITICAL: Read the schema file FIRST before creating HTML:**
- Read `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/recipe-schema.md`
- Search project knowledge for the recipe content (ingredients and instructions)
- Create the HTML file following the EXACT template in recipe-schema.md

**Key Requirements:**
- Use `Filesystem:write_file` tool (NOT create_file)
- Put `itemprop="recipeIngredient"` on EACH individual ingredient `<li>` tag
- Put `itemprop="recipeInstructions"` on EACH individual instruction `<li>` tag
- Do NOT put itemprop on parent `<ul>`, `<ol>`, or `<h2>` tags
- Image: Always use `IMG_7689.JPG` (relative path)
- File naming: lowercase-with-hyphens.html (e.g., pici-aglio-e-olio.html)
- Save location: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta/`

## STEP 3: Update the Inventory File
Use `Filesystem:edit_file` tool to:
1. Change `- [ ]` to `- [x]` for the completed recipe
2. Update the statistics:
   - Increment "Completed" count by 1
   - Decrement "Missing" count by 1
   
Location: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta/recipe-inventory.md`

## STEP 4: Update the Index File
Use `Filesystem:edit_file` tool to:
- Add the new recipe link in alphabetical order
- Format: `<li><a href="Mastering Pasta/filename.html">Display Name</a></li>`

Location: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/mastering-pasta.html`

## IMPORTANT RULES
- **Do NOT skip ANY recipes** including base dough recipes, stocks, and sauces
- Follow the inventory order exactly - do the NEXT unchecked item
- **ALWAYS read recipe-schema.md before creating the HTML**
- After completing all 4 steps, tell me how many recipes remain
- Wait for me to say "continue" before proceeding to the next recipe

## KEY DIRECTORY LOCATIONS
- GitHub repo: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io`
- Recipe HTMLs folder: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta/`
- Inventory file: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta/recipe-inventory.md`
- Index file: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/mastering-pasta.html`
- Schema file: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/recipe-schema.md`

## START COMMAND
Start by reading the inventory file to find the next missing recipe, then proceed with all 4 steps.
