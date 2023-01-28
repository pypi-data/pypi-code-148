from pydantic import BaseModel, Extra
import datetime as dt
from typing import Union



################
#
# CCD_ is the prefix for all Pydantic classes
# to prevent namespace collision with the 
# protobuf generated classes.
#
################
CCD_BlockHash               = str
CCD_TransactionHash         = str
CCD_AccountAddress          = str
microCCD                    = int
CCD_BakerId                 = int
CCD_ModuleRef               = str
CCD_ContractEvent           = str
CCD_Memo                    = str
CCD_RegisteredData          = str
CCD_BakerSignatureVerifyKey = str
CCD_OpenStatus              = int
CCD_BakerElectionVerifyKey  = str
CCD_BakerAggregationVerifyKey = str
CCD_Parameter               = str
CCD_AmountFraction          = float
CCD_ReceiveName             = str
CCD_ContractAddress         = dict

class CCD_StakePendingChange_Reduce(BaseModel):
    new_stake: microCCD
    effective_time: dt.datetime

class CCD_StakePendingChange_Remove(BaseModel):
    effective_time: dt.datetime

class CCD_StakePendingChange(BaseModel):
    reduce: CCD_StakePendingChange_Reduce = None
    remove: CCD_StakePendingChange_Remove = None

class CCD_BakerStakePendingChange_Reduce(BaseModel):
    reduced_equity_capital: microCCD
    effective_time: dt.datetime

class CCD_BakerStakePendingChange_Remove(BaseModel):
    effective_time: dt.datetime

class CCD_BakerStakePendingChange(BaseModel):
    reduce: CCD_BakerStakePendingChange_Reduce = None
    remove: CCD_BakerStakePendingChange_Remove = None


class CCD_DelegatorInfo(BaseModel):
    account: CCD_AccountAddress
    stake: microCCD
    pending_change: CCD_StakePendingChange = None

# class ConccordiumDelegatorRewardPeriodInfo(BaseModel):
#     delegators: list(ConcordiumDelegatorInfo)


class CCD_CurrentPaydayStatus(BaseModel):
    baker_equity_capital: microCCD
    blocks_baked: int
    delegated_capital: microCCD
    effective_stake: microCCD
    finalization_live: bool
    lottery_power: float
    transaction_fees_earned: microCCD

class CCD_CommissionRates(BaseModel):
    baking: float
    finalization: float
    transaction: float

class CCD_BakerPoolInfo(BaseModel):
    commission_rates: CCD_CommissionRates
    url: str
    open_status: str
    
class CCD_PoolInfo(BaseModel):
    all_pool_total_capital: microCCD
    address: CCD_AccountAddress
    equity_capital: microCCD
    baker: int
    equity_pending_change: CCD_BakerStakePendingChange
    current_payday_info: CCD_CurrentPaydayStatus = None
    delegated_capital: microCCD
    delegated_capital_cap: microCCD
    pool_info: CCD_BakerPoolInfo
    poolType: str = None
    
class CCD_PassiveDelegationInfo(BaseModel):
    all_pool_total_capital: microCCD
    delegated_capital: microCCD
    current_payday_transaction_fees_earned: microCCD
    current_payday_delegated_capital: microCCD
    commission_rates: CCD_CommissionRates
    
    
class CCD_BlockInfo(BaseModel):
    block_arrive_time: dt.datetime
    block_baker: int = None
    block_hash: CCD_BlockHash
    block_height: int
    block_last_finalized_block: CCD_BlockHash
    block_parent_block: CCD_BlockHash
    block_receive_time: dt.datetime
    block_slot_number: int
    block_slot_time: dt.datetime
    block_era_block_height: int
    block_finalized: bool
    block_genesis_index: int
    block_transaction_count: int
    block_transactions_energy_cost: int
    block_transactions_size: int

class CCD_AccountTransactionEffects_None(BaseModel):
    transaction_type: int = None
    reject_reason: dict


class CCD_Address(BaseModel):
    account: CCD_AccountAddress = None
    contract: CCD_ContractAddress = None

class CCD_ContractInitializedEvent(BaseModel):
    contract_version: int
    origin_ref: CCD_ModuleRef
    address: CCD_ContractAddress
    amount: microCCD = 0
    init_name: str
    events: list[CCD_ContractEvent]

class CCD_InstanceUpdatedEvent(BaseModel):
    contract_version: int
    address: CCD_ContractAddress
    instigator: CCD_Address
    amount: microCCD
    parameter: CCD_Parameter
    receive_name: CCD_ReceiveName
    events: list[CCD_ContractEvent]

class CCD_ContractTraceElement_Interrupted(BaseModel):
    address: CCD_ContractAddress
    events: list[CCD_ContractEvent]

class CCD_ContractTraceElement_Resumed(BaseModel):
    address: CCD_ContractAddress
    success: bool

class CCD_ContractTraceElement_Transferred(BaseModel):
    sender: CCD_ContractAddress
    amount: microCCD
    receiver: CCD_AccountAddress

class CCD_ContractTraceElement(BaseModel):
    updated: CCD_InstanceUpdatedEvent = None
    transferred: CCD_ContractTraceElement_Transferred = None
    interrupted: CCD_ContractTraceElement_Interrupted = None
    resumed: CCD_ContractTraceElement_Resumed = None

class CCD_ContractUpdateIssued(BaseModel):
    effects: list[CCD_ContractTraceElement]

class CCD_BakerKeysEvent(BaseModel):
    baker_id: CCD_BakerId
    account: CCD_AccountAddress
    sign_key: CCD_BakerSignatureVerifyKey
    election_key: CCD_BakerElectionVerifyKey
    aggregation_key: CCD_BakerAggregationVerifyKey

class CCD_BakerAdded(BaseModel):
    keys_event: CCD_BakerKeysEvent
    stake: microCCD
    restake_earnings: bool

class CCD_AccountTransfer(BaseModel):
    amount: microCCD
    receiver: CCD_AccountAddress
    memo: CCD_Memo = None

class CCD_NewRelease(BaseModel):
    timestamp: dt.datetime
    amount: microCCD

class CCD_TransferredWithSchedule(BaseModel):
    receiver: CCD_AccountAddress
    amount: list[CCD_NewRelease]
    memo: CCD_Memo = None

class CCD_BakerStakeUpdatedData(BaseModel):
    baker_id: CCD_BakerId
    new_stake: microCCD
    increased: bool

class CCD_BakerStakeUpdated(BaseModel):
    update: CCD_BakerStakeUpdatedData

class CCD_BakerStakeIncreased(BaseModel):
    baker_id: CCD_BakerId
    new_stake: microCCD

class CCD_BakerStakeDecreased(BaseModel):
    baker_id: CCD_BakerId
    new_stake: microCCD

class CCD_BakerRestakeEarningsUpdated(BaseModel):
    baker_id: CCD_BakerId
    restake_earnings: bool

class CCD_BakerSetOpenStatus(BaseModel):
    baker_id: CCD_BakerId
    open_status: CCD_OpenStatus

class CCD_BakerSetMetadataUrl(BaseModel):
    baker_id: CCD_BakerId
    url: str

class CCD_BakerSetTransactionFeeCommission(BaseModel):
    baker_id: CCD_BakerId
    transaction_fee_commission: CCD_AmountFraction

class CCD_BakerSetBakingRewardCommission(BaseModel):
    baker_id: CCD_BakerId
    baking_reward_commission: CCD_AmountFraction

class CCD_BakerSetFinalizationRewardCommission(BaseModel):
    baker_id: CCD_BakerId
    finalization_reward_commission: CCD_AmountFraction

class CCD_BakerEvent(BaseModel):
    baker_added: CCD_BakerAdded = None
    baker_removed: CCD_BakerId = None
    baker_stake_increased: CCD_BakerStakeIncreased = None
    baker_stake_decreased: CCD_BakerStakeDecreased = None
    baker_restake_earnings_updated: CCD_BakerRestakeEarningsUpdated = None
    baker_keys_updated: CCD_BakerKeysEvent = None
    baker_set_open_status: CCD_BakerSetOpenStatus = None
    baker_set_metadata_url: CCD_BakerSetMetadataUrl = None
    baker_set_transaction_fee_commission: CCD_BakerSetTransactionFeeCommission = None
    baker_set_baking_reward_commission: CCD_BakerSetBakingRewardCommission = None
    baker_set_finalization_reward_commission: CCD_BakerSetFinalizationRewardCommission = None

class CCD_BakerConfigured(BaseModel):
    events: list[CCD_BakerEvent]

class CCD_AccountTransactionEffects(BaseModel):
    outcome: str
    none: CCD_AccountTransactionEffects_None = None
    module_deployed: CCD_ModuleRef = None
    contract_initialized: CCD_ContractInitializedEvent = None
    contract_update_issued: CCD_ContractUpdateIssued = None
    account_transfer: CCD_AccountTransfer = None
    transferred_with_schedule: CCD_TransferredWithSchedule = None
    data_registered : CCD_RegisteredData = None
    baker_added: CCD_BakerAdded= None
    baker_removed: CCD_BakerId = None
    baker_stake_updated: CCD_BakerStakeUpdated = None
    baker_configured: CCD_BakerConfigured = None

class CCD_AccountTransactionDetails(BaseModel):
    cost: microCCD
    sender: CCD_AccountAddress
    effects: CCD_AccountTransactionEffects
    
class CCD_AccountCreationDetails(BaseModel):
    credential_type: int
    address: CCD_AccountAddress
    reg_id: str # bytes, but will be converted

class CCD_UpdateDetails(BaseModel):
    effective_time: dt.datetime
    payload: dict

class CCD_Transaction(BaseModel):
    index: int
    energy_cost: int
    hash: CCD_TransactionHash
    account_transaction: CCD_AccountTransactionDetails = None
    account_creation: CCD_AccountCreationDetails = None
    update: CCD_UpdateDetails = None
    
class CCD_Block(BaseModel):
    transaction_summaries: list[CCD_Transaction]

class AccountReleaseScheduleNodes(BaseModel):
    nodes: list

class CCD_AccountReleaseSchedule(BaseModel):
    schedules: list
    total: str
    
    
class DelegationTarget(BaseModel, extra=Extra.ignore):
    bakerId: int = None
    delegateType: str = None
    
class AccountDelegation(BaseModel):
    delegationTarget: DelegationTarget
    delegatorId: int = None
    restakeEarnings: bool
    stakedAmount: int

class BakerStakePendingChange(BaseModel):
    bakerEquityCapital: int = None
    effectiveTime: str = None
    pendingChangeType: str

class CurrentPaydayStatus(BaseModel):
    bakerEquityCapital: int
    blocksBaked: int
    delegatedCapital: int
    effectiveStake: int
    finalizationLive: bool
    lotteryPower: float
    transactionFeesEarned: int
    
# class AccountBakerPoolStatus(BaseModel):
#     allPoolTotalCapital: int
#     bakerAddress: str = None
#     bakerEquityCapital: int = None
#     bakerId: int = None
#     bakerStakePendingChange: BakerStakePendingChange = None
#     currentPaydayDelegatedCapital: int = None
#     currentPaydayTransactionFeesEarned: int = None
#     currentPaydayStatus: CurrentPaydayStatus = None
#     delegatedCapital: int
#     delegatedCapitalCap: int = None
#     # poolInfo: PoolInfo = None
#     commissionRates: CommissionRates = None
#     poolType: str


class CCD_BakerInfo(BaseModel):
    aggregation_key: str
    election_key: str
    baker_id: int
    signature_key: str

class CCD_AccountStakingInfo_Baker(BaseModel):
    baker_info: CCD_BakerInfo
    pool_info: CCD_BakerPoolInfo
    pending_change: CCD_StakePendingChange
    restake_earnings: bool
    staked_amount: microCCD

class CCD_DelegationTarget(BaseModel):
    baker_id: int = None
    passive: str = None

class CCD_AccountStakingInfo_Delegator(BaseModel):
    target: CCD_DelegationTarget
    pending_change: CCD_StakePendingChange
    restake_earnings: bool
    staked_amount: microCCD

class CCD_AccountStakingInfo(BaseModel):
    baker: CCD_AccountStakingInfo_Baker = None
    delegator: CCD_AccountStakingInfo_Delegator = None

class CCD_AccountInfo(BaseModel):
    account_address: str
    account_amount: microCCD
    account_stake: CCD_AccountStakingInfo = None
    account_credentials: list
    # accountEncryptionKey: str
    account_index: int
    account_schedule: CCD_AccountReleaseSchedule = None
    account_threshold: int
    
class CCD_TokenomicsInfo_V0(BaseModel):
    total_amount: microCCD
    total_encrypted_amount: microCCD
    baking_reward_account: microCCD
    finalization_reward_account: microCCD
    gas_account: microCCD
    protocol_version: int

class CCD_TokenomicsInfo_V1(BaseModel):
    total_amount: microCCD
    total_encrypted_amount: microCCD
    baking_reward_account: microCCD
    finalization_reward_account: microCCD
    gas_account: microCCD
    foundation_transaction_rewards: microCCD
    next_payday_time: dt.datetime
    next_payday_mint_rate: float
    total_staked_capital: microCCD
    protocol_version: int


class CCD_TokenomicsInfo(BaseModel):
    v0: CCD_TokenomicsInfo_V0 = None
    v1: CCD_TokenomicsInfo_V1 = None