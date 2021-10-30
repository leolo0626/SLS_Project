import pandas as pd



# def total_gain_t(initial_val, initial_price, price_t, constant) :
#     return ((price_t / initial_price) ** constant + (price_t / initial_price) ** -constant - 2) * initial_val / constant

def gain_t(initial_val, initial_price, price_t, constant):
    return ((price_t / initial_price) ** constant - 1) * initial_val / constant



if __name__ == "__main__" :
    price = pd.read_csv("data/XOM.csv")

    price = price.set_index("Date")

    selectedPrice = price[(price.index >= "2015-01-01") & (price.index <= "2016-10-31")]
    # selectedPrice = price
    # Plot Xom Price Data
    selectedPrice["Close"].plot()
    initial_val = 5000
    K_constant = 4
    initial_price = selectedPrice.loc[:, "Close"].iloc[0]
    selectedPrice.loc[:, "Gain"] = selectedPrice["Close"].apply(lambda x: gain_t(initial_val, initial_price, x, K_constant) +
                                                                   gain_t(-initial_val, initial_price, x, -K_constant))
    selectedPrice.loc[:, "Gain_Long"] = selectedPrice["Close"].apply(lambda x: gain_t(initial_val, initial_price, x, K_constant))
    selectedPrice.loc[:, "Gain_Short"] = selectedPrice["Close"].apply(lambda x: gain_t(-initial_val, initial_price, x, -K_constant))
    selectedPrice[["Gain", "Gain_Long", "Gain_Short"]].plot()
    selectedPrice["InvestmentLvl_Long"] = initial_val + selectedPrice["Gain_Long"] * K_constant
    selectedPrice["InvestmentLvl_Short"] = -initial_val + selectedPrice["Gain_Short"] * -K_constant
    selectedPrice[["InvestmentLvl_Long", "InvestmentLvl_Short"]].plot()
    selectedPrice["InvestmentLvl"] = selectedPrice["InvestmentLvl_Long"] + selectedPrice["InvestmentLvl_Short"]
    selectedPrice["InvestmentLvl"].plot()