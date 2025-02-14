import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

plt.style.use('bmh')


def plot_column(df, column_name, plot_kwargs=None, subplot_threshold=10,
                   symbol_column='symbol', datetime_column='datetime'):
    """Plot time series data from a DataFrame with symbol grouping.

    This function creates either a single plot with multiple lines or a grid of subplots,
    depending on the number of unique symbols in the data. If the number of symbols exceeds
    the subplot_threshold, it switches to a subplot view for better visibility.

    Args:
        df (pandas.DataFrame): DataFrame containing the time series data
        column_name (str): Name of the column to plot on the y-axis
        plot_kwargs (dict, optional): Additional keyword arguments to pass to plt.plot()
        subplot_threshold (int, optional): Maximum number of symbols before switching to subplots.
            Defaults to 10.
        symbol_column (str, optional): Name of the column containing symbol identifiers.
            Defaults to 'symbol'.
        datetime_column (str, optional): Name of the column containing datetime values.
            Defaults to 'datetime'.

    Raises:
        ValueError: If the DataFrame is missing required datetime or symbol columns

    Returns:
        None: Displays the plot but does not return any value
    """
    # Ensure datetime and symbol columns exist
    if datetime_column not in df.columns or symbol_column not in df.columns:
        raise ValueError("DataFrame must have 'datetime' and 'symbol' columns")
    if plot_kwargs is None:
        plot_kwargs = {}
    # Get unique symbols from the index
    symbols = df[symbol_column].unique()
    if len(symbols) > subplot_threshold:
        # Warn user about large number of symbols
        logger.warning(f"Large number of symbols ({len(symbols)}). Switching to subplot view for better visibility.")
        # Calculate grid dimensions for subplots
        n_symbols = len(symbols)
        n_cols = min(3, n_symbols)  # Max 3 columns for readability on HD screens
        n_rows = (n_symbols + n_cols - 1) // n_cols  # Ceiling division
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        axes = axes.flatten() if n_symbols > 1 else [axes]
        # Plot each symbol in its own subplot
        for i, symbol in enumerate(symbols):
            # Get data for this symbol
            symbol_data = df.query(f"{symbol_column} == @symbol")
            
            # Plot the data for this symbol
            axes[i].plot(symbol_data[datetime_column], symbol_data[column_name], **plot_kwargs)
            
            # Customize each subplot
            axes[i].set_title(f'{symbol}', pad=15)
            axes[i].set_xlabel('Date', labelpad=10)
            axes[i].set_ylabel(column_name, labelpad=10)
            axes[i].grid(True)
            axes[i].tick_params(axis='x', rotation=45)
        
        # Hide any unused subplots
        for j in range(i+1, len(axes)):
            axes[j].set_visible(False)
            
        # Add overall title
        plt.suptitle(f'`{column_name}` Over Time by Symbol')
        
        plt.tight_layout()
    else:
        plt.figure(figsize=(10, 6))

        # Plot each symbol's data
        for symbol in symbols:
            # Get data for this symbol
            symbol_data = df.query(f"{symbol_column} == @symbol")
            
            # Plot the data for this symbol
            plt.plot(symbol_data[datetime_column], symbol_data[column_name], label=symbol, **plot_kwargs)
        
        # Customize the plot
        plt.title(f'`{column_name}` Over Time by Symbol', pad=15)
        plt.xlabel('Date', labelpad=10)
        plt.ylabel(column_name, labelpad=10)
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Adjust layout with more bottom padding
        plt.tight_layout()
    return plt
