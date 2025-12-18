# Frontend (Flutter)

The frontend for Tendy is a Flutter app located at `frontend/myapp`.

Quick start (Web):

1. Install Flutter (https://docs.flutter.dev/get-started/install).
2. cd frontend/myapp
3. Update `lib/config.dart` `AppConfig.apiBaseUrl` to point to your backend (see comments in the file).
4. Run `flutter pub get`.
5. Run `flutter run -d chrome` to run the web build locally.

For Android / iOS, use an emulator/simulator or device and run `flutter run`.

Useful commands:

- `flutter analyze` — static analysis
- `flutter test` — widget/unit tests
- `flutter build web` — build a web release

Notes:
- The app communicates with the backend at `AppConfig.apiBaseUrl`. When testing from an Android emulator, use `10.0.2.2` as documented in `lib/config.dart`.
- If the backend is running in Docker on your machine, use your host's LAN IP for real devices.

Contributing:
- Add clear doc comments (///) to public widgets and API wrappers.
- Run `flutter analyze` before opening a PR.
