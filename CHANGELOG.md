# BStats changelog
All notable contributions and changes to the project will be documented here.

### 1.1.1 - 24th Jul 2022
#### Updated
- `Profile.club` now optionally returns `None` if the player is in no club.
### 1.1.0 - 10th Jul 2022
#### Added
- `ends_in` property to `EventSlot`.

#### Updated
- `AsyncClient` was renamed to `Client` and is the only supported client (asynchronous).
- `Event` was renamed to `EventDetails` and `Rotation` was renamed to `EventSlot`.

#### Removed
- `use_cache` parameter, cache usage is now defaulted (for easier access, without excessive API request spam).
- `SyncClient` has been removed. 

### 1.0.6 - 10th Jan 2022
#### Updated
- Replaced `self.client.session` with `requests.Session()` in the `club` attribute of the `Profile` object to eliminate possible errors.

### 1.0.5 - 10th Jan 2022
#### Updated
- `club` attribute for the `Profile` object used 2 arguments when in fact it accepts only 1.

### 1.0.4 - 10th Jan 2022
#### Added
- `type` and `badge_id` properties for the `Club` object.

### 1.0.3 - 10th Jan 2022
#### Added
- Import all errors in the \_\_init__ file.

### 1.0.2 - 9th Jan 2022
#### Added
- President property for the `Club` object.

### 1.0.1 - 9th Jan 2022
#### Added
- Dependencies for package installation.

### 1.0.0 - 9th Jan 2022
- **_Project release!_** 🎉
