# currently the update functions replace current values with the app arg
# need to figure out how we want to approach adding items or removing items from byteslices

from pyteal import *

def approval_program():
    on_creation = Seq(
        [
            # 1 g byteslice - Identity Owner's Algorand Address
            App.globalPut(Bytes("Soulbound_Identity_Owner"), Txn.application_args[0]),
            # 2 g byteslice - DAO Helper Username
            App.globalPut(Bytes("DAO_Helper_Username"), Bytes("")),
            # 3 g byteslice - Name ??? Don't think we use their name b/c of anonymity
            App.globalPut(Bytes("Name"), Bytes("")),
            # 4 g byteslice - Email Address
            App.globalPut(Bytes("Email_Address"), Bytes("")),
            # 5 g byteslice - ETH Wallet Addresses
            App.globalPut(Bytes("ETH_Wallet_Addresses"), Bytes("")),
            # 6 g byteslice - NEAR Wallet Addresses
            App.globalPut(Bytes("NEAR_Wallet_Addresses"), Bytes("")),
            # 7 g byteslice - DAOs and Memberships
            App.globalPut(Bytes("DAOs_Memberships"), Bytes("")),
            # 8 g byteslice - NFTs and Badges
            App.globalPut(Bytes("NFTs_Badges"), Bytes("")),
            # 9 g byteslice - Skills
            App.globalPut(Bytes("Skills"), Bytes("")),
            # 10 g byteslice - Tasks Completed
            App.globalPut(Bytes("Tasks_Completed"), Bytes("")),
            # 11 g byteslice - Tokens
            App.globalPut(Bytes("Tokens"), Bytes("")),
            # 1 g int - Hours Worked
            App.globalPut(Bytes("Hours_Worked"), Int(0)),
            # approve sequence
            Return(Int(1)),
        ]
    )

    opt_in = Seq(
        [
            # must be creator to opt in 
            Assert(Txn.sender() == Global.creator_address()),
            # approve opt in
            Return(Int(1)),
        ]
    )

    on_closeout = Seq(
        [
            # must be creator to opt in 
            Assert(Txn.sender() == Global.creator_address()),
            # approve closeout
            Return(Int(1)),
        ]
    )

    update_dao_helper_username = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("DAO_Helper_Username"), Txn.application_args[1]),
            # approves sequence
            Return(Int(1)),
        ]
    )

    update_name = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("Name"), Txn.application_args[1]),
            # approves sequence
            Return(Int(1)),
        ]
    )

    update_email_address = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("Email_Address"), Txn.application_args[1]),
            # approves sequence
            Return(Int(1)),
        ]
    )

    update_eth_wallet_addresses = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("ETH_Wallet_Addresses"), Txn.application_args[1]),
            # approves sequence
            Return(Int(1)),
        ]
    )

    update_near_wallet_addresses = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("Near_Wallet_Addresses"), Txn.application_args[1]),
            # approves sequence
            Return(Int(1)),
        ]
    )

    update_daos_memberships = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("DAOs_Memberships"), Txn.application_args[1]),
            # approves sequence
            Return(Int(1)),
        ]
    )

    update_nfts_badges = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("NFTs_Badges"), Txn.application_args[1]),
            # approves sequence
            Return(Int(1)),
        ]
    )

    update_skills = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("Skills"), Txn.application_args[1]),
            # approves sequence
            Return(Int(1)),
        ]
    )

    update_tasks_completed = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("Tasks_Completed"), Txn.application_args[1]),
            # approves sequence
            Return(Int(1)),
        ]
    )

    update_tokens = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("Tokens"), Txn.application_args[1]),
            # approves sequence
            Return(Int(1)),
        ]
    )

    update_hours_worked = Seq(
        [
            # requires two app args (the noop call name and the credentials)
            Assert(Txn.application_args.length() == Int(2)),
            # changes the credentials global state with the second app arg in the array
            App.globalPut(Bytes("Hours_Worked"), App.globalGet(Bytes("Hours_Worked")) + Btoi(Txn.application_args[1])),
            # approves sequence
            Return(Int(1)),
        ]
    )

    is_soulbound_addr = Txn.sender() == App.globalGet(Bytes("Soulbound_Identity_Owner"))

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_soulbound_addr)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_soulbound_addr)],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        [Txn.on_completion() == OnComplete.OptIn, opt_in],
        [Txn.application_args[0] == Bytes("Update_DAO_Helper_Username"), update_dao_helper_username],
        [Txn.application_args[0] == Bytes("Update_Name"), update_name],
        [Txn.application_args[0] == Bytes("Update_Email_Address"), update_email_address],
        [Txn.application_args[0] == Bytes("Update_ETH_Wallet_Addresses"), update_eth_wallet_addresses],
        [Txn.application_args[0] == Bytes("Update_Near_Wallet_Addresses"), update_near_wallet_addresses],
        [Txn.application_args[0] == Bytes("Update_DAOs_Memberships"), update_daos_memberships],
        [Txn.application_args[0] == Bytes("Update_NFTs_Badges"), update_nfts_badges],
        [Txn.application_args[0] == Bytes("Update_Skills"), update_skills],
        [Txn.application_args[0] == Bytes("Update_Tasks_Completed"), update_tasks_completed],
        [Txn.application_args[0] == Bytes("Update_Tokens"), update_tokens],
        [Txn.application_args[0] == Bytes("Update_Hours_Worked"), update_hours_worked],
    )

    return program

def clear_state_program():
    program = Seq(
        [
            Return(Int(1)),
        ]
    )

    return program


if __name__ == "__main__":
    with open("identity_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled)

    with open("identity_clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled)