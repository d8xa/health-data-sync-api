
# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [1.0.2] - 2023-07-01
 
### Added

- Better JSON schema, now with sub-schemas for all possible data categories (metrics, workouts, symptoms, ECG).

### Changed

- Changed hardcoded volume path to environment variable in compose file
- Cleaned up Docker build process
- Restructured project

 
### Fixed

 
## [1.0.1] - 2023-06-23
 
### Added

- Added `MAX_CONTENT_LENGTH` as environment variable to be read into the config.
 
### Changed
 
### Fixed
 
- Removed illegal character from savename of saved files.
 

## [1.0.0] - 2023-06-13
 
### Added

- Docker support
   
### Changed
 
### Fixed