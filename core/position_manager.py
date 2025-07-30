# core/position_manager.py

def open_perp_position(drift_client, market_index, direction, size, leverage):
    # direction: "long" or "short"
    drift_client.open_position(
        market_index=market_index,
        direction=direction,
        base_asset_amount=size,
        leverage=leverage
    )

def close_perp_position(drift_client, market_index):
    drift_client.close_position(market_index)
