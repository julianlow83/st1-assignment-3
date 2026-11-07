"""Run the supplied demo or the Stage 9 interactive menu."""

import argparse

from smartcare.console import run_demo, run_menu
from smartcare.data_store import SmartCareDataStore  # 1. Import SmartCareDataStore

def main() -> None:
    """Run the demo, or the interactive menu using a shared data store."""
    parser = argparse.ArgumentParser(
        description='SmartCare teaching application',
    )
    parser.add_argument('--interactive', action='store_true')
    args = parser.parse_args()

    # 2. Instantiate a shared session data store
    store = SmartCareDataStore()

    if args.interactive:
        try:
            run_menu(store)  # 3. Pass the store to run_menu
        except NotImplementedError as error:
            print(error)
    else:
        run_demo(store)  # (Optional, but best practice for demo too)

if __name__ == '__main__':
    main()