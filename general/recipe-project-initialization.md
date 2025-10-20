# Recipe Project Initialization Guide

This guide provides step-by-step instructions for initializing a new recipe HTML project from a cookbook.

---

## Overview

When a user asks to "initialize a new recipe project" or start a new cookbook project, follow these steps to set up the complete project structure, navigation, and tracking files.

---

## Information to Gather First

Before starting, ask the user for the following information:

1. **Cookbook/Project Name** - What should the project be called? (e.g., "The Essential Cuban Cookbook")
2. **Recipe Folder Name** - What should the recipe folder be called in the github folder? (Usually the cookbook name)
3. **Cover Image Location** - Where is the reusable cover image located? What is its filename?
4. **Source Location** - Where are the cookbook images/PDFs located? (e.g., `/Users/michelle/Documents/recipes/[Cookbook Name]`)
5. **Table of Contents Location** - Where are the table of contents images located?

---

## Step-by-Step Initialization Process

### Step 1: Create the Recipe Folder

Create the main recipe folder in the github folder where all recipe HTML files will be stored.

**Action:**
```
Use Filesystem:create_directory to create:
/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/[Recipe Folder Name]
```

**Definition:** This folder will be referred to as "the recipe folder"

---

### Step 2: Move the Cover Image

Locate and move/copy the reusable cover image into the recipe folder.

**Actions:**
1. Use `Filesystem:list_directory` to verify the cover image exists at the source location
2. Use `Filesystem:move_file` to move it to the recipe folder
   - Source: [User-provided location]/[Image filename]
   - Destination: /Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/[Recipe Folder Name]/[Image filename]

**Note:** If move fails, the image might already be in use. Try copying instead using bash or ask the user.

---

### Step 3: Create the Project Definitions File

Create a definitions file in the recipe folder to document all project paths and terminology.

**Action:**
Use `Filesystem:write_file` to create:
`/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/[Recipe Folder Name]/project-definitions.md`

**Content template:**
```markdown
# Project Definitions - [Cookbook Name]

## Project Paths

1. **GitHub Folder** = `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io`

2. **Recipe Folder** = `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/[Recipe Folder Name]`

3. **Cover Image** = `[Image filename]` (located in the recipe folder)

4. **Image Folder** = `/Users/michelle/Documents/recipes/[Cookbook Name]/images`

5. **Table of Contents Folder** = `/Users/michelle/Documents/recipes/[Cookbook Name]/table of contents`

6. **Inventory** / **Inventory File** = `recipe-inventory.md` (located in the recipe folder)

7. **Index** / **Index File** = `[cookbook-name-lowercase].html` (located in the github folder) - the main index page for [Cookbook Name] recipes

8. **Master Index** = `index.html` (located in the github folder) - the master collection index linking to all cookbook indexes

---

## Reference Project (Mastering Pasta)
- Recipe HTMLs location: `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/Mastering Pasta`
- Index file: `file:///Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/mastering-pasta.html`
- Master index: `file:///Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/index.html`
- Inventory file: `recipe-inventory.md` (in Mastering Pasta folder)
- Cover image: `IMG_7689.JPG`

---

*Created: [Current Date]*
```

---

### Step 4: Create the Recipe Inventory File

Read the table of contents images from Project Knowledge and create a comprehensive inventory of all recipes.

**Actions:**
1. Use `project_knowledge_search` with queries like:
   - "table of contents [Cookbook Name]"
   - "chapter one contents"
   - "chapter two contents"
   - etc.

2. Extract all recipe names and page numbers from the returned images

3. Use `Filesystem:write_file` to create:
   `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/[Recipe Folder Name]/recipe-inventory.md`

**Content template:**
```markdown
# [Cookbook Name] - Recipe Inventory

**Last updated:** [Current Date]

## Progress Statistics
- **Total recipes:** [X]
- **Completed:** 0
- **Missing:** [X]
- **Progress:** 0%

---

## Chapter [Number] - [CHAPTER NAME]

- [ ] Recipe Name / English Name (p.XX)
- [ ] Recipe Name / English Name (p.XX)

---

## Chapter [Number] - [CHAPTER NAME]

- [ ] Recipe Name / English Name (p.XX)

---

## Notes

### File Naming Convention
HTML files use lowercase with hyphens, e.g., `recipe-name.html`

---

## Recipe File Locations

All HTML files will be stored in:
`/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/[Recipe Folder Name]/`

Main index file (to be created):
`/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/[cookbook-name-lowercase].html`
```

**Key Points:**
- Each recipe should be unchecked `- [ ]` initially
- Include page numbers from the cookbook
- Organize by chapters/sections as they appear in the table of contents
- Count total recipes accurately

---

### Step 5: Create the Index File

Create the main recipe index page that will list all recipe links (currently empty).

**Actions:**
1. Read the Mastering Pasta index as a template:
   `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/mastering-pasta.html`

2. Use `Filesystem:write_file` to create:
   `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/[cookbook-name-lowercase].html`

**Content template:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Cookbook Name] - Recipe Index</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #333;
        }
        .back-link {
            display: inline-block;
            margin-bottom: 20px;
            color: #0066cc;
            text-decoration: none;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .recipe-list {
            list-style: none;
            padding: 0;
        }
        .recipe-list li {
            margin: 8px 0;
        }
        .recipe-list a {
            display: block;
            padding: 10px;
            background-color: #f9f9f9;
            text-decoration: none;
            color: #333;
            border-radius: 3px;
            transition: background-color 0.3s;
        }
        .recipe-list a:hover {
            background-color: #e8e8e8;
        }
    </style>
</head>
<body>
    <a href="index.html" class="back-link">← Back to Recipe Collection</a>
    <h1>[Cookbook Name]</h1>
    <ul class="recipe-list">
        <!-- Recipe links will be added here as they are created -->
    </ul>
</body>
</html>
```

**Definition:** This file is "the index"

---

### Step 6: Update the Master Index

Add a link to the new cookbook index in the master recipe collection index.

**Actions:**
1. Read the current master index:
   `/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io/index.html`

2. Use `Filesystem:edit_file` to add the new cookbook link in **alphabetical order**

3. Format: `<a href="[cookbook-name-lowercase].html" class="book-link">[Cookbook Name]</a>`

**Example edit:**
```
Old:
    <h1>Recipe Collection</h1>
    <a href="mastering-pasta.html" class="book-link">Mastering Pasta</a>
</body>

New:
    <h1>Recipe Collection</h1>
    <a href="essential-cuban-cookbook.html" class="book-link">The Essential Cuban Cookbook</a>
    <a href="mastering-pasta.html" class="book-link">Mastering Pasta</a>
</body>
```

**Definition:** This file is "the master index"

---

## Verification Checklist

After completing all steps, verify:

- [ ] Recipe folder created in github folder
- [ ] Cover image is in the recipe folder
- [ ] Project definitions file created with all 8 definitions
- [ ] Inventory file created with all recipes from table of contents
- [ ] Index file created (empty but ready for recipe links)
- [ ] Master index updated with link to new cookbook
- [ ] All definitions properly documented

---

## Summary Response to User

After completing initialization, provide the user with a summary:

```
✅ Project initialization complete!

I have successfully:
1. Created the recipe folder: [path]
2. Moved the cover image ([filename]) into the recipe folder
3. Created the project definitions file with 8 key definitions
4. Created the recipe inventory with [X] recipes organized by chapter
5. Created the index file (currently empty, ready for recipe links)
6. Updated the master index to include [Cookbook Name]

The project is now ready for recipe creation!
```

---

## Common Issues and Solutions

**Issue:** Cover image cannot be moved
**Solution:** The image might be in use or the source path might be incorrect. Ask the user to verify the location or use bash to copy instead of move.

**Issue:** Table of contents images not found in Project Knowledge
**Solution:** Ask the user to upload the table of contents images to Project Knowledge first, or upload them directly to the chat.

**Issue:** Cannot determine total recipe count
**Solution:** Count carefully from all chapter images. If uncertain, provide best estimate and note it can be updated later.

---

## Important Notes

- Always use `Filesystem:write_file` and `Filesystem:edit_file` tools, not `create_file`
- Use the `project_knowledge_search` tool to access cookbook images that have been uploaded to Project Knowledge
- Recipe folder names should match the cookbook name but may be customized by the user
- Index filenames should be lowercase with hyphens (e.g., `essential-cuban-cookbook.html`)
- Always maintain alphabetical order in the master index
- The definitions file is critical - it establishes terminology for the entire project

---

## Questions to Ask During Initialization

Before starting, ask the user:

1. "What is the name of the cookbook/project?"
2. "What should I name the recipe folder? (Default: cookbook name)"
3. "Where is the reusable cover image located, and what is its filename?"
4. "Have the table of contents images been uploaded to Project Knowledge? If not, please upload them now."
5. "Where are the cookbook images stored? (e.g., `/Users/michelle/Documents/recipes/[Cookbook Name]`)"

---

*This guide was created on October 20, 2025 for initializing recipe HTML projects from cookbooks.*
