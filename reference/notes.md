* Install Workflow
  * Generate executable with PyInstaller (https://pyinstaller.org/en/stable/)
  * Create windows installer with Inno Setup (https://jrsoftware.org/isinfo.php)


* Project Notes
  * How do we allow the users to create and edit elements?
    * Option 1: Modals
      * Create a modal for each type of item that can be created
        * We can add some code re-use if we design the inner widgets to have some concept of read-only
        * This means we need to manage showing the window and handling if the content has changed when the window closes
        * This does not allow easy comparisons to the existing type of data since we do not get the entire object back from the modal
        * This also creates a lot of pop-up windows for the user to manage and interact with
    * Option 2: In-Line
      * Use the tab widgets to edit each component inline
      * We will need to handle how to ensure the DB is always updated after each change
        * Possibly some concept of if the element is dirty?
          * If it is dirty, how do we want to update the DB? Update or delete and re-insert?

* DB Changes that need to be ade
  * Remove the builtin/custom specialization for materials
    * Just add an extra column for custom vs builtin
  * Figure out a better relationship for tanks and facilities