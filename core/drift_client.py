# core/drift_client.py

from driftpy.drift_client import DriftClient
from driftpy.wallet import Wallet
from solana.rpc.api import Client as SolanaClient
import os

def init_drift_client(keypair_path: str, rpc_url: str):
    solana_client = SolanaClient(rpc_url)
    wallet = Wallet(keypair_path)
    drift_client = DriftClient(solana_client, wallet)
    return drift_client
