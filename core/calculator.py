"""
Real Estate Calculator — utility functions for financial metrics
These run locally without API calls for instant results
"""


class RealEstateCalculator:
    
    @staticmethod
    def gross_rental_yield(annual_rent: float, purchase_price: float) -> float:
        """Gross rental yield as percentage"""
        if purchase_price <= 0:
            return 0
        return round((annual_rent / purchase_price) * 100, 2)
    
    @staticmethod
    def net_rental_yield(annual_rent: float, purchase_price: float, expense_ratio: float = 0.35) -> float:
        """Net yield after expenses (default 35% expense ratio)"""
        net_income = annual_rent * (1 - expense_ratio)
        return RealEstateCalculator.gross_rental_yield(net_income, purchase_price)
    
    @staticmethod
    def cap_rate(noi: float, property_value: float) -> float:
        """Capitalization rate"""
        if property_value <= 0:
            return 0
        return round((noi / property_value) * 100, 2)
    
    @staticmethod
    def price_to_rent_ratio(purchase_price: float, monthly_rent: float) -> float:
        """Price-to-rent ratio (lower = better for buying)"""
        if monthly_rent <= 0:
            return 0
        return round(purchase_price / (monthly_rent * 12), 1)
    
    @staticmethod
    def monthly_mortgage(principal: float, annual_rate: float, years: int = 25) -> float:
        """Monthly mortgage payment"""
        monthly_rate = annual_rate / 100 / 12
        n = years * 12
        if monthly_rate == 0:
            return principal / n
        payment = principal * (monthly_rate * (1 + monthly_rate)**n) / ((1 + monthly_rate)**n - 1)
        return round(payment, 2)
    
    @staticmethod
    def cash_on_cash_return(annual_cash_flow: float, cash_invested: float) -> float:
        """Cash-on-cash return percentage"""
        if cash_invested <= 0:
            return 0
        return round((annual_cash_flow / cash_invested) * 100, 2)
    
    @staticmethod
    def appreciation_projection(purchase_price: float, years: int, rate: float) -> dict:
        """Project property value at different timepoints"""
        projections = {}
        for year in [1, 3, 5, 10, 20]:
            if year <= years or year == years:
                future_value = purchase_price * ((1 + rate/100) ** year)
                gain = future_value - purchase_price
                projections[f"{year}yr"] = {
                    "value": round(future_value, 0),
                    "gain": round(gain, 0),
                    "gain_pct": round((gain / purchase_price) * 100, 1)
                }
        return projections
    
    @staticmethod
    def break_even_years(purchase_price: float, monthly_rent: float, 
                         expense_ratio: float = 0.35, appreciation_rate: float = 5.0) -> float:
        """Estimate years to break even including appreciation"""
        annual_net_income = monthly_rent * 12 * (1 - expense_ratio)
        # Simple calculation: when cumulative income + appreciation covers costs
        year = 0
        cumulative = 0
        while cumulative < purchase_price and year < 50:
            year += 1
            current_value = purchase_price * ((1 + appreciation_rate/100) ** year)
            cumulative = annual_net_income * year + (current_value - purchase_price)
        return year
    
    @staticmethod
    def investment_score_from_metrics(gross_yield: float, cap_rate_val: float, 
                                       ptr_ratio: float) -> float:
        """Generate a quick financial health score 0-10"""
        score = 0
        
        # Gross yield scoring (good yield = 6%+)
        if gross_yield >= 8:
            score += 3.5
        elif gross_yield >= 6:
            score += 2.5
        elif gross_yield >= 4:
            score += 1.5
        elif gross_yield >= 2:
            score += 0.5
        
        # Cap rate scoring (good = 5%+)
        if cap_rate_val >= 7:
            score += 3.5
        elif cap_rate_val >= 5:
            score += 2.5
        elif cap_rate_val >= 3:
            score += 1.5
        elif cap_rate_val >= 1:
            score += 0.5
        
        # Price-to-rent ratio (lower is better; <15 is excellent, 20+ is expensive)
        if ptr_ratio < 12:
            score += 3
        elif ptr_ratio < 15:
            score += 2
        elif ptr_ratio < 20:
            score += 1
        
        return min(round(score, 1), 10)
