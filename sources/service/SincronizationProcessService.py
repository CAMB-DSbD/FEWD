from srcFewd.service.PBBService import PBBService
from srcFewd.KiT.KiT import main as kit_main

class SincronizationProcessService:
    def display_sync_menu(self):
        print("Select Synchronization Protocol")
        print("1. PBB Synchronization")
        print("2. KIT Synchronization")
        option = int(input("Enter an option: "))
        if option == 1:
            self.pbb_synchronization()
        elif option == 2:
            self.start_kit_synchronization()
        else:
            print("Invalid option. Please try again.")
            self.display_sync_menu()

    def pbb_synchronization(self):

        print("Starting PBB synchronization...")
        pbbService = PBBService()
        #pbbService.syncA_syncB()
        #pbbService.syncA_cancelA_SyncB()
        #pbbService.syncA_cancelB()
        #pbbService.cancelA_syncB()

        #############################
        # pbbService.syncB_syncA()
        # pbbService.syncB_cancelB_SyncA()
        # pbbService.syncB_cancelA()
        pbbService.cancelB_syncA()


    # def menu_cases(self):
    #     while True:
    #         print("Submenu:")
    #         print("1. S_a/S_b")
    #         print("2. C_a/S_b")
    #         print("3. C_a/C_b")
    #         print("4. S_b/C_b/S_a")
    #         print("0. Return to main menu")
    #         option = int(input("Enter an option: "))
    #         if option == 1:
    #             print("Starting PBB synchronization...")
    #             pbbService = PBBService()
    #             pbbService.syncA_syncB()
    #         elif option == 2:
    #             print("Starting PBB synchronization...")
    #             pbbService = PBBService()
    #             pbbService.canceLA_syncB()
    #
    #             # Add your logic for Option 2 here
    #         elif option == 3:
    #             print("Starting PBB synchronization...")
    #             pbbService = PBBService()
    #             pbbService.canceLA_cancelB()
    #             # Add your logic for Option 3 here
    #         elif option == 4:
    #             print("Starting PBB synchronization...")
    #             pbbService = PBBService()
    #             pbbService.syncB_cancelB_SyncA()
    #         elif option == 0:
    #             break
    #         else:
    #             print("Invalid option. Please try again.")


    def start_kit_synchronization(self):
        print("Starting KIT synchronization...")
        kit_main()