import pandas as pd
import config


def refresh_analysis():
    # reading data
    print("Performing analysis")
    league_data = pd.read_csv(config.local_storage + config.raw_data + ".csv")
    league_data["weighting"] = 1

    expected_types = list(config.mapping_dictionary.values())
    # aggregating all actions into player data
    print("Calculating player stats")
    pivoted_league_data = league_data.groupby(["Player", "type", "Team"]).count()
    pivoted_league_data = (
        pd.pivot_table(
            pivoted_league_data,
            index=["Player", "Team"],
            columns="type",
            values="weighting",
        )
        .reindex(columns=expected_types, fill_value=0)
        .fillna(0)
        .astype(int)
    )

    pivoted_league_data["Total Goals"] = (
        pivoted_league_data["Field Goal"]
        + pivoted_league_data["Penalty Corner"]
        + pivoted_league_data["Penalty Stroke"]
    )
    pivoted_league_data = pivoted_league_data.reset_index()
    pivoted_league_data = pivoted_league_data.sort_values(
        "Total Goals", ascending=False
    )
    field_order = [
        "Player",
        "Team",
        "Green Card",
        "Yellow Card",
        "Red Card",
        "Penalty Stroke",
        "Penalty Corner",
        "Field Goal",
        "Total Goals",
    ]
    pivoted_league_data = pivoted_league_data[field_order]
    pivoted_league_data = pivoted_league_data.fillna(0)
    pivoted_league_data.to_csv(
        config.local_storage + config.analysed_player_filename + ".csv", index=False
    )

    # aggregating all actions further into team data
    print("Calculating team stats")
    team_data = league_data.groupby(["type", "Team"]).count()
    team_data = (
        pd.pivot_table(team_data, index="Team", columns="type", values="weighting")
        .reindex(columns=expected_types, fill_value=0)
        .fillna(0)
        .astype(int)
    )

    # renaming fields
    rename_dictionary = {
        "Green Card": "Green Card Conceded",
        "Yellow Card": "Yellow Card Conceded",
        "Red Card": "Red Card Conceded",
        "Penalty Stroke": "Penalty Stroke Scored",
        "Penalty Corner": "Penalty Corner Scored",
        "Field Goal": "Field Goal Scored",
    }
    team_data = team_data.rename(columns=rename_dictionary)

    team_data["Total Goals Scored"] = (
        team_data["Field Goal Scored"]
        + team_data["Penalty Corner Scored"]
        + team_data["Penalty Stroke Scored"]
    )

    other_team_data = league_data.groupby(["type", "Other Team"]).count()
    other_team_data = (
        pd.pivot_table(
            other_team_data, index="Other Team", columns="type", values="weighting"
        )
        .reindex(columns=expected_types, fill_value=0)
        .fillna(0)
        .astype(int)
    )
    rename_dictionary = {
        "Green Card": "Green Card Drawn",
        "Yellow Card": "Yellow Card Drawn",
        "Red Card": "Red Card Drawn",
        "Penalty Stroke": "Penalty Stroke Conceded",
        "Penalty Corner": "Penalty Corner Conceded",
        "Field Goal": "Field Goal Conceded",
    }
    other_team_data = other_team_data.rename(columns=rename_dictionary)
    other_team_data["Total Goals Conceded"] = (
        other_team_data["Field Goal Conceded"]
        + other_team_data["Penalty Corner Conceded"]
        + other_team_data["Penalty Stroke Conceded"]
    )

    full_team_data = pd.merge(
        team_data, other_team_data, left_index=True, right_index=True, how="left"
    )

    full_team_data["Goal Difference"] = (
        full_team_data["Total Goals Scored"] - full_team_data["Total Goals Conceded"]
    )
    full_team_data = full_team_data.sort_values("Goal Difference", ascending=False)

    field_order = [
        "Green Card Conceded",
        "Yellow Card Conceded",
        "Red Card Conceded",
        "Penalty Stroke Conceded",
        "Penalty Corner Conceded",
        "Field Goal Conceded",
        "Total Goals Conceded",
        "Green Card Drawn",
        "Yellow Card Drawn",
        "Red Card Drawn",
        "Penalty Stroke Scored",
        "Penalty Corner Scored",
        "Field Goal Scored",
        "Total Goals Scored",
        "Goal Difference",
    ]

    full_team_data = full_team_data[field_order]

    full_team_data.to_csv(config.local_storage + config.analysed_team_filename + ".csv")
