import pandas as pd
import matplotlib.pyplot as plt

def plot_progress():

    file_path = "data/health_history.csv"

    try:
        df = pd.read_csv(file_path, parse_dates=["Date"])
    except FileNotFoundError:
        print("No progress data found. Record your first session to generate history.")
        return
    except Exception as exc:
        print(f"Unable to load progress data: {exc}")
        return

    if len(df) == 0:
        print("No progress data available yet. Record your first session to generate history.")
        return

    if len(df) == 1:
        print("Only one historical record exists. Keep logging progress to see trends.")
        print(f"Wellness Score: {df['WellnessScore'].iloc[0]}")

        plt.figure()
        plt.plot(df["Date"], df["WellnessScore"], marker="o")
        plt.xlabel("Date")
        plt.ylabel("Wellness Score")
        plt.title("Wellness Progress Over Time")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        return

    # 🔥 TREND MESSAGE
    if df["WellnessScore"].iloc[-1] > df["WellnessScore"].iloc[-2]:
        print("📈 Your health is improving!")
    else:
        print("⚠️ Your health needs attention!")

    plt.figure()
    plt.plot(df["Date"], df["WellnessScore"], marker="o")
    plt.xlabel("Date")
    plt.ylabel("Wellness Score")
    plt.title("Wellness Progress Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_weekly_progress():

    file_path = "data/health_history.csv"

    try:
        df = pd.read_csv(file_path, parse_dates=["Date"])
    except FileNotFoundError:
        print("No progress data found. Record your first session to generate history.")
        return
    except Exception as exc:
        print(f"Unable to load progress data: {exc}")
        return

    if len(df) == 0:
        print("No progress data available yet. Record your first session to generate history.")
        return

    df["WeekStart"] = df["Date"] - pd.to_timedelta(df["Date"].dt.weekday, unit="d")
    weekly_columns = [
        "WeeklySleep",
        "WeeklyStress",
        "WeeklyMood",
        "WeeklyScreenTime",
        "WeeklySedentary",
        "WeeklyRecovery"
    ]
    for column in weekly_columns:
        if column not in df.columns:
            df[column] = pd.NA

    weekly = df.groupby("WeekStart", sort=True).agg(
        WellnessScore=("WellnessScore", "mean"),
        WeeklySleep=("WeeklySleep", "mean"),
        WeeklyStress=("WeeklyStress", "mean"),
        WeeklyMood=("WeeklyMood", "mean"),
        WeeklyScreenTime=("WeeklyScreenTime", "mean"),
        WeeklySedentary=("WeeklySedentary", "mean"),
        WeeklyRecovery=("WeeklyRecovery", "mean")
    ).reset_index()

    if weekly["WeekStart"].nunique() == 0 or weekly[weekly_columns].notna().sum().sum() == 0:
        print("No weekly input data available. Please submit weekly progress data first.")
        return

    week_labels = weekly["WeekStart"].dt.strftime("%Y-%m-%d")

    if len(weekly) == 1:
        print("Only one week of progress is recorded. Keep logging weekly data to build a trend.")

    fig, axes = plt.subplots(4, 1, figsize=(10, 14), sharex=True)

    axes[0].plot(week_labels, weekly["WellnessScore"], marker="o", color="#1f77b4")
    axes[0].set_title("Weekly Wellness Score")
    axes[0].set_ylabel("Wellness Score")

    axes[1].plot(week_labels, weekly["WeeklySleep"], marker="o", label="Sleep (hrs)")
    axes[1].plot(week_labels, weekly["WeeklyScreenTime"], marker="o", label="Screen Time (hrs)")
    axes[1].set_title("Weekly Sleep and Screen Time")
    axes[1].set_ylabel("Hours")
    axes[1].legend()

    axes[2].plot(week_labels, weekly["WeeklyStress"], marker="o", label="Stress")
    axes[2].plot(week_labels, weekly["WeeklyMood"], marker="o", label="Mood")
    axes[2].set_title("Weekly Stress and Mood")
    axes[2].set_ylabel("Score")
    axes[2].legend()

    axes[3].plot(week_labels, weekly["WeeklySedentary"], marker="o", label="Sedentary (hrs)")
    axes[3].plot(week_labels, weekly["WeeklyRecovery"], marker="o", label="Recovery (hrs)")
    axes[3].set_title("Weekly Sedentary and Recovery")
    axes[3].set_ylabel("Hours")
    axes[3].set_xlabel("Week Starting")
    axes[3].legend()

    for ax in axes:
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()