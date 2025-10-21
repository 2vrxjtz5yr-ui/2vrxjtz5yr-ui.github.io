# THE ESSENTIAL CUBAN COOKBOOK - RECIPE HTML CREATION GUIDE

## PROJECT OVERVIEW
This project converts recipes from "The Essential Cuban Cookbook" into HTML files that can be imported into recipe management software. The HTML files must use proper Schema.org markup with itemprop attributes on individual list items (NOT parent elements) or the import will fail.

## CRITICAL CONTEXT FROM TROUBLESHOOTING
- **The `create_file` tool does NOT work** for this file system - always use `Filesystem:write_file`
- **Schema.org markup MUST be on individual `<li>` tags** - putting itemprop on parent `<ul>`, `<ol>`, or `<h2>` tags will cause the recipe to import as "1 ingredient" with no instructions
- **Each recipe takes one completion** - trying to do multiple recipes in one response causes crashes due to token limits
- **Wait for user confirmation** between recipes to avoid crashes

---

## FILE PATHS AND STRUCTURE

**For complete project definitions and terminology, see:**
`/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/project-definitions.md`

**Critical paths to use:**
- Recipe HTML files: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/[recipe-name].html`
- Main index file: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/essential-cuban-cookbook.html`
- Inventory file: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/recipe-inventory.md`
- Cover image reference: `IMG_7890.JPG` (relative path in HTML)

**Always use these exact paths - do not check or verify, just use them directly.**

**Definitions:**
- **Recipe Folder** = `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/`
- **Index** = `essential-cuban-cookbook.html` (the main recipe index)
- **Master Index** = `index.html` (the collection of all cookbook indexes)
- **Inventory** = `recipe-inventory.md` (tracks recipe completion status)
- **GitHub Folder** = `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/`

---

## HOW RECIPE IMAGES ARE ACCESSED

**CRITICAL: The cookbook page images MUST be uploaded to Project Knowledge first.**

### Setup (Done Once Per Cookbook)

**Before starting recipe creation:** Upload all cookbook page images to the Project's Knowledge base
1. Go to Project Settings → Knowledge
2. Upload the images from the local filesystem (e.g., `/Users/michelle/Documents/recipes/The Essential Cuban Cookbook/images/`)
3. Wait for upload to complete

### Accessing Recipes During Creation

**To read a recipe:**

1. **Use the `project_knowledge_search` tool** with a query containing:
   - Recipe name (both Spanish and English if applicable)
   - Page number (if known)
   - Key ingredients or terms from the recipe
   
   Example query: `"Tostadas Cubanas Cuban Toast page 4"`

2. **The tool will return image results** showing pages from the cookbook
   - These images come from Project Knowledge (NOT the filesystem)
   - The images contain the actual recipe text
   - You can read the ingredients, instructions, and descriptions directly from these images
   - Multiple images may be returned if the recipe spans multiple pages

3. **Extract the recipe information** from the images:
   - Read the ingredient list with quantities
   - Read the step-by-step instructions
   - Note any headnotes, descriptions, or cultural notes
   - Look for "Variation Tip," "Ingredient Tip," or "Technique Tip" boxes

**Example workflow:**

```
User: "Make Tostadas Cubanas"

You: [calls project_knowledge_search with query "Tostadas Cubanas Cuban Toast page 4"]

Tool returns: [Images from Project Knowledge showing cookbook pages with the recipe]

You: [Read the images to extract:]
- Title: Tostadas Cubanas / Cuban Toast
- Prep/Cook Time: if provided
- Yield: Makes X servings
- Ingredients: butter, Cuban bread, etc.
- Instructions: Step 1, Step 2, Step 3...
- Description: [Any intro text about the dish]

Then: [Create HTML file using this extracted information]
```

### Important Notes

- **Claude CANNOT directly read image files from the filesystem** using paths like `/Users/michelle/Documents/recipes/The Essential Cuban Cookbook/images/IMG_7920.JPG`
- The images MUST be in Project Knowledge first
- The `project_knowledge_search` tool is specifically designed to search the project's uploaded content
- You CAN read text from images returned by the tool - they are photographs of cookbook pages with clearly readable text
- Always search for the recipe first - don't try to recall recipes from memory
- If the first search doesn't return the recipe, try different keywords or terms

### Alternative if Project Knowledge is Not Available

If `project_knowledge_search` tool is not available in the conversation:
1. Ask the user to upload the specific cookbook page images directly to the chat
2. Once uploaded to the chat, you can view and read those images
3. Extract the recipe information and proceed with HTML creation

---

## HANDLING RECIPE VARIATIONS

**CRITICAL: All variations must be created as separate, standalone recipe files.**

When a recipe includes variations (e.g., a base recipe with "Variation Tip" suggesting alternatives):

1. **Create the base recipe first** with its full instructions
2. **Create each variation as its own complete standalone recipe file** if it's listed separately in the inventory
   - Use a descriptive filename
   - Include complete ingredients and instructions (adapted from base recipe)
   - Explain what makes this variation different in the description
   
**Why this matters:** Users searching for a specific variation won't know to search for the base recipe. Each variation that appears in the inventory needs its own searchable file.

---

## THE 4-STEP PROCESS

### STEP 1: Find the Next Recipe
1. Read the inventory file: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/recipe-inventory.md`
2. Find the NEXT missing recipe (first one with `- [ ]` checkbox)
3. Note the recipe name (both Spanish and English names) and page number

### STEP 2: Create the HTML File

**BEFORE writing ANY HTML, read the schema requirements below!**

#### Search for Recipe Content

Use the `project_knowledge_search` tool to find the recipe:
- Query with recipe name (Spanish and/or English), page number, and key terms
- Read the returned images to extract all recipe details
- Note ingredients, instructions, descriptions, and any tips or variations

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
        <img itemprop="image" src="IMG_7890.JPG" alt="The Essential Cuban Cookbook cover" style="max-width: 100%; height: auto; margin-bottom: 20px;">
        
        <h1 itemprop="name">[Spanish Name / English Name]</h1>
        
        <div class="recipe-meta">
            <span itemprop="recipeYield">[X] servings</span>
            <!-- Include prep/cook time if provided in recipe -->
        </div>

        <div class="description" itemprop="description">
            <p>[Recipe description from cookbook]</p>
            
            <!-- CRITICAL: Include ALL tips (Variation/Ingredient/Technique) as paragraphs within the description section -->
            <p><strong>Ingredient Tip:</strong> [Tip text if applicable]</p>
            
            <p><strong>Technique Tip:</strong> [Tip text if applicable]</p>
            
            <p><strong>Variation Tip:</strong> [Tip text if applicable]</p>
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
            <p><strong>Source:</strong> Recipe from <em>The Essential Cuban Cookbook</em></p>
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
- **File naming:** lowercase-with-hyphens.html (e.g., `tostadas-cubanas.html`)
- **Save location:** `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/`

### STEP 3: Update the Inventory File

Use `Filesystem:edit_file` tool to make TWO edits:

**Edit 1: Mark recipe as complete**
- Change `- [ ] Recipe Name (p.XXX)` to `- [x] Recipe Name (p.XXX)`

**Edit 2: Update statistics**
- Find the line `- **Completed:** XX`
- Increment by 1
- Find the line `- **Missing:** XX`
- Decrement by 1

**Location:** `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/recipe-inventory.md`

### STEP 4: Update the Index File

Use `Filesystem:edit_file` tool or rewrite the entire file to:
- Add the new recipe link in **alphabetical order**
- Format: `        <li><a href="The Essential Cuban Cookbook/filename.html">Display Name</a></li>`
- Note: 8 spaces of indentation to match existing entries
- Use the English name for the display text

**When adding multiple recipes:** It's easier to read the entire index file and rewrite it with all recipes in correct alphabetical order rather than doing multiple string replacements.

**Location:** `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/essential-cuban-cookbook.html`

---

## BATCH PROCESSING TIPS

When creating multiple recipes in one session:

**Do create files immediately** - Don't plan first, create as you go
**Do update inventory after each batch** - Not after every single recipe
**Do update index at the end** - Easier to add multiple entries at once in alphabetical order
**Don't ask for permission** - Just create the recipes as requested

**Typical batch size:** 5 recipes at a time works well

---

## MANAGING THE INDEX

The index (`essential-cuban-cookbook.html`) should be updated in alphabetical order.

**When adding multiple recipes:**
1. Read the current index file
2. Identify where each new recipe belongs alphabetically (by English name)
3. Rewrite the entire file with all recipes in correct alphabetical order
4. Don't use string replacement - it's error-prone with multiple insertions

**Alphabetization rules:**
- Use the English name for alphabetization
- Numbers come first if any
- Ignore articles (The, A, An) if present
- Special characters: accents are alphabetized normally (é = e)

---

## COMPLETION CHECKLIST

After finishing all 4 steps:
- [ ] HTML file created with correct Schema.org markup (itemprop on individual `<li>` tags)
- [ ] Inventory file updated (checkbox and statistics)
- [ ] Index file updated (recipe added in alphabetical order)
- [ ] Told user how many recipes remain
- [ ] **WAIT for user to say "continue" before doing the next recipe** (unless working in batches)

---

## IMPORTANT RULES

1. **Do NOT skip ANY recipes** - Include all recipes from the inventory
2. **Follow inventory order exactly** - Do the NEXT unchecked item, not random ones
3. **One recipe per completion OR batch of 5** - Never try to do too many recipes at once (causes crashes)
4. **Always use Filesystem:write_file** - The create_file tool doesn't work for this
5. **Read the inventory first** - Always start by reading the inventory to find the next recipe
6. **Wait for confirmation** - After completing a recipe (or batch), wait for user to say "continue"
7. **Create separate HTML files for ALL recipe variations** - If a variation is listed separately in the inventory
8. **Images must be in Project Knowledge** - Cannot read images directly from filesystem paths
9. **Use both Spanish and English names** - Include both names in the H1 title

---

## COMMON ISSUES TO AVOID

❌ **Don't**: Try to read images from filesystem paths like `/Users/michelle/Documents/recipes/...`
✅ **Do**: Use `project_knowledge_search` to access images from Project Knowledge

❌ **Don't**: Check if paths exist or verify file structure
✅ **Do**: Use the exact paths specified above confidently

❌ **Don't**: Use placeholder content
✅ **Do**: Write complete instructions from the cookbook

❌ **Don't**: Put itemprop on `<ul>`, `<ol>`, or `<h2>` tags
✅ **Do**: Put itemprop on each individual `<li>` tag

❌ **Don't**: Use `create_file` tool
✅ **Do**: Use `Filesystem:write_file` tool

❌ **Don't**: Alphabetize by Spanish names
✅ **Do**: Alphabetize by English names in the index

---

## KEY FILE LOCATIONS

| File | Path |
|------|------|
| **Recipe source** | **Project Knowledge (images uploaded to project - use `project_knowledge_search` tool)** |
| **Source images (reference)** | `/Users/michelle/Documents/recipes/The Essential Cuban Cookbook/images/` (must be uploaded to Project Knowledge first) |
| Inventory | `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/recipe-inventory.md` |
| Recipe HTMLs | `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/` |
| Index file | `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/essential-cuban-cookbook.html` |
| This guide | `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/recipe-creation-guide.md` |
| Project definitions | `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/The Essential Cuban Cookbook/project-definitions.md` |

---

## COMMON MISTAKES TO AVOID

| Mistake | Why It Breaks | Solution |
|---------|---------------|----------|
| Using `create_file` | File doesn't actually get created | Use `Filesystem:write_file` |
| `itemprop` on `<ul>` or `<ol>` | Import sees 1 ingredient, no instructions | Put `itemprop` on each `<li>` |
| `itemprop` on `<h2>` | Instructions don't import | Put `itemprop` on each `<li>` |
| Trying to do too many recipes | Token limit causes crash | Do batches of ~5 recipes |
| Skipping recipes | Inventory gets out of sync | Follow inventory order exactly |
| Checking/verifying paths | Wastes time | Just use the specified paths |
| Reading images from filesystem | Cannot view images this way | Use `project_knowledge_search` tool |

---

## EXAMPLE WORKFLOW

**User says:** "Make the next 5 recipes"

**You do:**
1. Read inventory file
2. Find next 5 unchecked recipes
3. For each recipe:
   - Search project knowledge using `project_knowledge_search` with recipe name and page number
   - Read the images returned to extract recipe details (ingredients, instructions, descriptions)
   - Create HTML using `Filesystem:write_file` with proper schema
4. Update inventory (mark all 5 complete, update stats)
5. Update index (add all 5 links in alphabetical order by English name)
6. Say: "✅ Completed 5 recipes: [list them]. 47 recipes remaining. Ready to continue when you say 'continue'."

**You wait** - Don't automatically start the next batch

---

## TROUBLESHOOTING

### If `project_knowledge_search` tool is not available:
1. Inform the user that the tool is not available in this conversation
2. Ask the user to either:
   - Upload the specific cookbook page images to the chat, OR
   - Ensure images are uploaded to Project Knowledge and restart the conversation
3. Once images are uploaded to the chat, you can view and read them to extract recipe information

### If search returns no results:
1. Try different keywords or broader terms
2. Try searching with just the page number
3. Try both Spanish and English names
4. Ask user to confirm the recipe name and page number
5. As last resort, ask user to upload the specific page image to the chat

---

## START COMMAND

To begin: Read the inventory file and proceed with Step 1 to find the next missing recipe.
