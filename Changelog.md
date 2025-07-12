# Changelog

## [2.4.0] - 2025-07-12

### Fixed
- Fixed a critical bug where the multi-select feature in the file manager was only returning a single file instead of all selected files. The `_confirm_selection` method was refactored to correctly gather all selected file paths when in multi-select mode.

## [2.3.0] - 2025-07-12

### Fixed
- Fixed a critical bug where the multi-select feature in the file manager was only returning a single file instead of all selected files.

## [2.2.0] - 2025-07-12

### Changed
- Improved the file manager's multi-select functionality with a dedicated "Start Multi-Select" button for a more intuitive user experience.
- Restored the original navigation behavior of the "Select" button for single-file selection and folder navigation.

## [2.1.0] - 2025-07-12

### Added
- Logging to the application using a custom logger module.
- `logger.py` file for centralized logging configuration.

### Changed
- Updated `app.py` and `file_manager.py` to include logging statements for better debugging and monitoring.
- Improved the file manager's user experience by:
    - Changing the cursor to a pointer when hovering over the file list.
    - Separating navigation and selection actions for clearer user interaction.
- Reworked the main application window to have separate buttons for selecting a file and a destination folder, providing a more intuitive workflow.

### Fixed
- Fixed an issue where the file manager would automatically scroll to the top after selecting an item.
- Fixed a bug that caused the file manager to relaunch unexpectedly after a selection was made.