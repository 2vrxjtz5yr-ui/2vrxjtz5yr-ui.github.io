# MASTERING PASTA RECIPE HTML CREATION - COMPLETE GUIDE

## PROJECT OVERVIEW
This project converts recipes from the "Mastering Pasta" cookbook by Marc Vetri into HTML files that can be imported into recipe management software. The HTML files must use proper Schema.org markup with itemprop attributes on individual list items (NOT parent elements) or the import will fail.

## CRITICAL CONTEXT FROM TROUBLESHOOTING
- **The `create_file` tool does NOT work** for this file system - always use `Filesystem:write_file`
- **Schema.org markup MUST be on individual `<li>` tags** - putting itemprop on parent `<ul>`, `<ol>`, or `<h2>` tags will cause the recipe to import as "1 ingredient" with no instructions
- **Each recipe takes one completion** - trying to do multiple recipes in one response causes crashes due to token limits
- **Wait for user confirmation** between recipes to avoid crashes

---

## THE 4-STEP PROCESS

### STEP 1: Find the Next Recipe
1. Read the inventory file: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta/recipe-inventory.md`
2. Find the NEXT missing recipe (first one with `- [ ]` checkbox)
3. Note the recipe name and page number

### STEP 2: Create the HTML File

**BEFORE writing ANY HTML, read the schema requirements below!**

#### Search for Recipe Content
- Use `project_knowledge_search` tool with the recipe name and page number
- Extract all ingredients and instructions from the search results

#### Create HTML Using This EXACT Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Recipe Name]</title>
    <style>
        body {
            font-family: Georgia, serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }
        h1 {
            color: #8B4513;
            font-size: 2em;
            margin-bottom: 10px;
        }
        .recipe-meta {
            color: #666;
            font-style: italic;
            margin-bottom: 20px;
        }
        .description {
            margin: 20px 0;
            font-size: 1.1em;
        }
        h2 {
            color: #8B4513;
            margin-top: 30px;
            border-bottom: 2px solid #8B4513;
            padding-bottom: 5px;
        }
        ul, ol {
            padding-left: 30px;
        }
        li {
            margin-bottom: 10px;
        }
        .note {
            background-color: #f9f4ef;
            padding: 15px;
            border-left: 4px solid #8B4513;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <article itemscope itemtype="http://schema.org/Recipe">
        <img itemprop="image" src="IMG_7689.JPG" alt="Mastering Pasta cookbook cover" style="max-width: 100%; height: auto; margin-bottom: 20px;">
        
        <h1 itemprop="name">[Recipe Name]</h1>
        
        <div class="recipe-meta">
            <span itemprop="recipeYield">[X] servings</span>
        </div>

        <div class="description" itemprop="description">
            <p>[Recipe description from cookbook]</p>
        </div>

        <!-- OPTIONAL: Only include if there's a pasta swap note in the recipe -->
        <div class="note">
            <strong>Pasta Swap:</strong> [Pasta swap text if applicable]
        </div>

        <h2>Ingredients</h2>
        <ul>
            <li itemprop="recipeIngredient">[ingredient 1]</li>
            <li itemprop="recipeIngredient">[ingredient 2]</li>
            <li itemprop="recipeIngredient">[ingredient 3]</li>
            <!-- CRITICAL: Each <li> must have itemprop="recipeIngredient" -->
        </ul>

        <h2>Instructions</h2>
        <ol>
            <li itemprop="recipeInstructions">[instruction step 1]</li>
            <li itemprop="recipeInstructions">[instruction step 2]</li>
            <li itemprop="recipeInstructions">[instruction step 3]</li>
            <!-- CRITICAL: Each <li> must have itemprop="recipeInstructions" -->
        </ol>

        <div class="note">
            <p><strong>Source:</strong> Recipe from <em>Mastering Pasta: The Art and Practice of Handmade Pasta, Gnocchi, and Risotto</em> by Marc Vetri with David Joachim</p>
        </div>
    </article>
</body>
</html>
```

#### CRITICAL SCHEMA.ORG REQUIREMENTS

**❌ WRONG - This breaks the import:**
```html
<!-- DO NOT put itemprop on parent elements -->
<ul itemprop="recipeIngredient">
    <li>ingredient 1</li>
    <li>ingredient 2</li>
</ul>

<h2>Instructions</h2>
<ol>
    <li>step 1</li>
    <li>step 2</li>
</ol>
```

**✅ CORRECT - This works:**
```html
<!-- Put itemprop on EACH individual list item -->
<ul>
    <li itemprop="recipeIngredient">ingredient 1</li>
    <li itemprop="recipeIngredient">ingredient 2</li>
</ul>

<h2>Instructions</h2>
<ol>
    <li itemprop="recipeInstructions">step 1</li>
    <li itemprop="recipeInstructions">step 2</li>
</ol>
```

**FORMATTING REMINDER:**
- Keep instruction steps as separate `<li>` items - don't combine multiple steps
- Include blank lines between `<li>` tags for readability in the HTML source

#### Save the File
- **Tool to use:** `Filesystem:write_file` (NOT create_file)
- **File naming:** lowercase-with-hyphens.html (e.g., `pici-aglio-e-olio.html`)
- **Save location:** `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta/`

### STEP 3: Update the Inventory File

Use `Filesystem:edit_file` tool to make TWO edits:

**Edit 1: Mark recipe as complete**
- Change `- [ ] Recipe Name (p.XXX)` to `- [x] Recipe Name (p.XXX)`

**Edit 2: Update statistics**
- Find the line `- **Completed:** XX`
- Increment by 1
- Find the line `- **Missing:** XX`
- Decrement by 1

**Location:** `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta/recipe-inventory.md`

### STEP 4: Update the Index File

Use `Filesystem:edit_file` tool to:
- Add the new recipe link in **alphabetical order**
- Format: `        <li><a href="Mastering Pasta/filename.html">Display Name</a></li>`
- Note: 8 spaces of indentation to match existing entries

**Location:** `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/mastering-pasta.html`

---

## COMPLETION CHECKLIST

After finishing all 4 steps:
- [ ] HTML file created with correct Schema.org markup (itemprop on individual `<li>` tags)
- [ ] Inventory file updated (checkbox and statistics)
- [ ] Index file updated (recipe added in alphabetical order)
- [ ] Told user how many recipes remain
- [ ] **WAIT for user to say "continue" before doing the next recipe**

---

## IMPORTANT RULES

1. **Do NOT skip ANY recipes** - Include base dough recipes, stocks, sauces, everything
2. **Follow inventory order exactly** - Do the NEXT unchecked item, not random ones
3. **One recipe per completion** - Never try to do multiple recipes at once (causes crashes)
4. **Always use Filesystem:write_file** - The create_file tool doesn't work for this
5. **Read the inventory first** - Always start by reading the inventory to find the next recipe
6. **Wait for confirmation** - After completing a recipe, wait for user to say "continue"

---

## KEY FILE LOCATIONS

| File | Path |
|------|------|
| Inventory | `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta/recipe-inventory.md` |
| Recipe HTMLs | `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta/` |
| Index file | `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/mastering-pasta.html` |
| This guide | `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/recipe-creation-prompt.md` |
| Schema reference | `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/recipe-schema.md` |

---

## COMMON MISTAKES TO AVOID

| Mistake | Why It Breaks | Solution |
|---------|---------------|----------|
| Using `create_file` | File doesn't actually get created | Use `Filesystem:write_file` |
| `itemprop` on `<ul>` or `<ol>` | Import sees 1 ingredient, no instructions | Put `itemprop` on each `<li>` |
| `itemprop` on `<h2>` | Instructions don't import | Put `itemprop` on each `<li>` |
| Trying to do multiple recipes | Token limit causes crash | Do one recipe, wait for "continue" |
| Skipping recipes | Inventory gets out of sync | Follow inventory order exactly |

---

## EXAMPLE WORKFLOW

**User says:** "Continue making recipes"

**You do:**
1. Read inventory file
2. Find next unchecked recipe (e.g., "Loriguittas with Seafood")
3. Search project knowledge for that recipe
4. Create HTML using Filesystem:write_file with proper schema
5. Update inventory (mark complete, update stats)
6. Update index (add link alphabetically)
7. Say: "✅ Completed Loriguittas with Seafood. 36 recipes remaining. Ready to continue with the next recipe when you say 'continue'."

**You wait** - Don't automatically start the next recipe

---

## START COMMAND

To begin: Read the inventory file and proceed with Step 1 to find the next missing recipe.
