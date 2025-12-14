"""
Portfolio visualization module for creating professional charts and dashboards.
Generates publication-ready visualizations for portfolio risk analysis.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def create_var_bar_chart(df, output_file='outputs/var_analysis.png'):
    """
    Create a bar chart showing VaR for each position with quality color coding.

    Args:
        df: Portfolio dataframe with VaR and quality ratings
        output_file: Path to save the chart
    """
    try:
        logger.info("Creating VaR bar chart...")

        # Sort by VaR
        df_sorted = df.sort_values('Var', ascending=True)

        # Map quality to colors
        color_map = {'GOOD': '#35FC03', 'MID': '#FFFF00', 'BAD': '#FC2C03', 'UNKNOWN': '#808080'}
        colors = [color_map.get(qual, '#808080') for qual in df_sorted['Qual']]

        # Create figure
        fig, ax = plt.subplots(figsize=(14, 8))

        # Create bar chart
        bars = ax.barh(df_sorted['Symbol'], df_sorted['Var'], color=colors, edgecolor='black', linewidth=0.5)

        # Customize
        ax.set_xlabel('Value at Risk (VaR) - 1 Day, 95% Confidence', fontsize=12, fontweight='bold')
        ax.set_ylabel('Stock Symbol', fontsize=12, fontweight='bold')
        ax.set_title('Portfolio Value at Risk Analysis\nRisk Distribution by Position',
                     fontsize=16, fontweight='bold', pad=20)

        # Add grid
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#35FC03', edgecolor='black', label='GOOD (Low Risk)'),
            Patch(facecolor='#FFFF00', edgecolor='black', label='MID (Medium Risk)'),
            Patch(facecolor='#FC2C03', edgecolor='black', label='BAD (High Risk)')
        ]
        ax.legend(handles=legend_elements, loc='lower right', framealpha=0.9)

        # Format x-axis as currency
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        logger.info(f"VaR bar chart saved to {output_file}")

    except Exception as e:
        logger.error(f"Error creating VaR bar chart: {e}")
        raise


def create_portfolio_dashboard(df, output_file='outputs/portfolio_dashboard.png'):
    """
    Create a comprehensive 4-panel dashboard showing portfolio metrics.

    Args:
        df: Portfolio dataframe with all metrics
        output_file: Path to save the dashboard
    """
    try:
        logger.info("Creating portfolio dashboard...")

        # Create figure with subplots
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # 1. Sector Allocation (Top Left)
        ax1 = fig.add_subplot(gs[0, 0])
        sector_allocation = df.groupby('Sector')['Protfilio Precentage'].sum().sort_values(ascending=False)
        colors_sector = plt.cm.Set3(np.linspace(0, 1, len(sector_allocation)))
        wedges, texts, autotexts = ax1.pie(
            sector_allocation,
            labels=sector_allocation.index,
            autopct='%1.1f%%',
            colors=colors_sector,
            startangle=90,
            textprops={'fontsize': 10}
        )
        ax1.set_title('Sector Allocation', fontsize=14, fontweight='bold', pad=15)

        # 2. Position Sizes (Top Right)
        ax2 = fig.add_subplot(gs[0, 1])
        df_positions = df.nlargest(10, 'Protfilio Precentage')[['Symbol', 'Protfilio Precentage']].sort_values('Protfilio Precentage')
        bars2 = ax2.barh(df_positions['Symbol'], df_positions['Protfilio Precentage'] * 100,
                         color='steelblue', edgecolor='black', linewidth=0.5)
        ax2.axvline(x=5, color='red', linestyle='--', linewidth=2, label='5% Limit')
        ax2.set_xlabel('Portfolio Percentage (%)', fontsize=11, fontweight='bold')
        ax2.set_title('Top 10 Position Sizes', fontsize=14, fontweight='bold', pad=15)
        ax2.legend()
        ax2.grid(axis='x', alpha=0.3)

        # 3. Long/Short Exposure (Middle Left)
        ax3 = fig.add_subplot(gs[1, 0])
        position_types = df.groupby('Position')['Protfilio Precentage'].sum()
        bars3 = ax3.bar(position_types.index, position_types.values * 100,
                        color=['#2ecc71', '#e74c3c'], edgecolor='black', linewidth=1.5)
        ax3.set_ylabel('Portfolio Percentage (%)', fontsize=11, fontweight='bold')
        ax3.set_title('Long vs Short Exposure', fontsize=14, fontweight='bold', pad=15)
        ax3.grid(axis='y', alpha=0.3)

        # Add percentage labels on bars
        for bar in bars3:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontweight='bold', fontsize=12)

        # 4. Quality Distribution (Middle Right)
        ax4 = fig.add_subplot(gs[1, 1])
        quality_counts = df.groupby('Qual').size()
        quality_order = ['GOOD', 'MID', 'BAD']
        quality_colors = {'GOOD': '#35FC03', 'MID': '#FFFF00', 'BAD': '#FC2C03'}

        # Filter to only existing qualities and maintain order
        existing_qualities = [q for q in quality_order if q in quality_counts.index]
        quality_values = [quality_counts[q] for q in existing_qualities]
        colors_quality = [quality_colors[q] for q in existing_qualities]

        bars4 = ax4.bar(existing_qualities, quality_values,
                        color=colors_quality, edgecolor='black', linewidth=1.5)
        ax4.set_ylabel('Number of Positions', fontsize=11, fontweight='bold')
        ax4.set_title('VaR Quality Distribution', fontsize=14, fontweight='bold', pad=15)
        ax4.grid(axis='y', alpha=0.3)

        # Add count labels on bars
        for bar in bars4:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold', fontsize=12)

        # 5. VaR Distribution Histogram (Bottom - spans both columns)
        ax5 = fig.add_subplot(gs[2, :])

        # Create bins and color them by quality
        n_bins = 20
        counts, bins, patches = ax5.hist(df['Var'], bins=n_bins, edgecolor='black', linewidth=0.5)

        # Color bins based on VaR thresholds
        var_sorted = df['Var'].sort_values()
        good_threshold = var_sorted.quantile(0.33)
        mid_threshold = var_sorted.quantile(0.90)

        for patch, left_edge in zip(patches, bins[:-1]):
            if left_edge < good_threshold:
                patch.set_facecolor('#35FC03')
            elif left_edge < mid_threshold:
                patch.set_facecolor('#FFFF00')
            else:
                patch.set_facecolor('#FC2C03')

        ax5.set_xlabel('Value at Risk (VaR)', fontsize=11, fontweight='bold')
        ax5.set_ylabel('Number of Positions', fontsize=11, fontweight='bold')
        ax5.set_title('VaR Distribution Across Portfolio', fontsize=14, fontweight='bold', pad=15)
        ax5.grid(axis='y', alpha=0.3)

        # Add vertical line for mean VaR
        mean_var = df['Var'].mean()
        ax5.axvline(x=mean_var, color='darkblue', linestyle='--', linewidth=2,
                    label=f'Mean VaR: ${mean_var:,.0f}')
        ax5.legend()

        # Format x-axis
        ax5.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Add main title
        fig.suptitle('Portfolio Risk Analysis Dashboard',
                     fontsize=18, fontweight='bold', y=0.98)

        # Add timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        fig.text(0.99, 0.01, f'Generated: {timestamp}',
                ha='right', va='bottom', fontsize=8, style='italic', alpha=0.7)

        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        logger.info(f"Portfolio dashboard saved to {output_file}")

    except Exception as e:
        logger.error(f"Error creating portfolio dashboard: {e}")
        raise


def create_risk_summary_card(df, output_file='outputs/risk_summary.png'):
    """
    Create a visual summary card with key portfolio metrics.

    Args:
        df: Portfolio dataframe
        output_file: Path to save the card
    """
    try:
        logger.info("Creating risk summary card...")

        # Calculate metrics
        total_positions = len(df)
        total_exposure = df['Protfilio Precentage'].sum()
        avg_var = df['Var'].mean()
        max_var = df['Var'].max()
        worst_stock = df.loc[df['Var'].idxmax(), 'Symbol']

        quality_counts = df.groupby('Qual').size()
        good_count = quality_counts.get('GOOD', 0)
        mid_count = quality_counts.get('MID', 0)
        bad_count = quality_counts.get('BAD', 0)

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')

        # Add title
        title_text = 'PORTFOLIO RISK SUMMARY'
        ax.text(0.5, 0.95, title_text, ha='center', va='top',
                fontsize=22, fontweight='bold', transform=ax.transAxes)

        # Create metric boxes
        metrics = [
            ('Total Positions', f'{total_positions}', 0.15),
            ('Portfolio Exposure', f'{total_exposure:.1%}', 0.40),
            ('Average VaR', f'${avg_var:,.0f}', 0.65),
        ]

        y_pos = 0.75
        for label, value, x_pos in metrics:
            # Draw box
            box = plt.Rectangle((x_pos-0.10, y_pos-0.08), 0.20, 0.15,
                               facecolor='lightblue', edgecolor='black',
                               linewidth=2, transform=ax.transAxes)
            ax.add_patch(box)

            # Add text
            ax.text(x_pos, y_pos+0.03, value, ha='center', va='center',
                   fontsize=20, fontweight='bold', transform=ax.transAxes)
            ax.text(x_pos, y_pos-0.04, label, ha='center', va='center',
                   fontsize=10, style='italic', transform=ax.transAxes)

        # Quality breakdown
        y_pos = 0.50
        ax.text(0.5, y_pos, 'Quality Breakdown', ha='center', va='center',
               fontsize=14, fontweight='bold', transform=ax.transAxes)

        y_pos = 0.35
        quality_data = [
            ('🟢 GOOD', good_count, '#35FC03', 0.2),
            ('🟡 MID', mid_count, '#FFFF00', 0.5),
            ('🔴 BAD', bad_count, '#FC2C03', 0.8),
        ]

        for label, count, color, x_pos in quality_data:
            # Draw circle
            circle = plt.Circle((x_pos, y_pos), 0.05, color=color,
                              edgecolor='black', linewidth=2, transform=ax.transAxes)
            ax.add_patch(circle)

            # Add count
            ax.text(x_pos, y_pos, str(count), ha='center', va='center',
                   fontsize=16, fontweight='bold', transform=ax.transAxes)

            # Add label
            ax.text(x_pos, y_pos-0.09, label, ha='center', va='center',
                   fontsize=10, transform=ax.transAxes)

        # Highest risk position
        y_pos = 0.15
        ax.text(0.5, y_pos, f'⚠️ Highest Risk Position: {worst_stock} (${max_var:,.0f} VaR)',
               ha='center', va='center', fontsize=12,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
               transform=ax.transAxes)

        # Add timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        ax.text(0.5, 0.02, f'Generated: {timestamp}',
               ha='center', va='bottom', fontsize=8, style='italic',
               alpha=0.7, transform=ax.transAxes)

        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        logger.info(f"Risk summary card saved to {output_file}")

    except Exception as e:
        logger.error(f"Error creating risk summary card: {e}")
        raise


def generate_all_visualizations(portfolio_path):
    """
    Generate all portfolio visualizations.

    Args:
        portfolio_path: Path to the portfolio Excel file with VaR data
    """
    try:
        # Create output directory
        import os
        os.makedirs('outputs', exist_ok=True)

        logger.info(f"Loading portfolio data from {portfolio_path}")
        df = pd.read_excel(portfolio_path)

        # Generate all visualizations
        create_var_bar_chart(df)
        create_portfolio_dashboard(df)
        create_risk_summary_card(df)

        logger.info("\n" + "="*60)
        logger.info("✅ All visualizations generated successfully!")
        logger.info("="*60)
        logger.info("Generated files:")
        logger.info("  📊 outputs/var_analysis.png - VaR bar chart")
        logger.info("  📈 outputs/portfolio_dashboard.png - Comprehensive dashboard")
        logger.info("  📋 outputs/risk_summary.png - Risk summary card")
        logger.info("="*60)
        logger.info("These visualizations are ready for LinkedIn/presentations!")
        logger.info("="*60 + "\n")

    except Exception as e:
        logger.error(f"Error generating visualizations: {e}")
        raise


if __name__ == '__main__':
    # For standalone testing
    import config
    generate_all_visualizations(config.PORTFOLIO_PATH_TRANSFORMED)
