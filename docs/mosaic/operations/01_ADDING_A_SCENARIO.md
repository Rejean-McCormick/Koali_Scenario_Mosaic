# Adding a Scenario

## Normal case

1. create the Markdown file;
2. create/assign its image;
3. write `preview_summary`;
4. validate palette/components/badges;
5. choose a free slot;
6. add the assignment to `mosaic-layout.json`;
7. run validation/build;
8. check the preview;
9. check the scenario page;
10. commit.

## Placement rule

The developer does not run a clustering algorithm. The editorial owner chooses the slot while looking at the overall composition.

## If no slot is satisfactory

- use a reserved peripheral slot;
- or create a new layout version if the addition is significant enough.

## Do not

- move 30 existing cells for one new scenario;
- write x/y coordinates inside Markdown;
- treat the slot ID as semantic meaning.
