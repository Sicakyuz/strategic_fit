import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def main():
    # Set page configuration
    st.set_page_config(page_title="Supply Chain Strategy Simulation",
                       layout="wide")

    # Function to calculate performance index based on multiple factors
    def calculate_performance(total_cost, lead_time, demand_uncertainty,
                              responsiveness_factor, sustainability_factor,
                              risk_factor, weights):
        """Calculate the strategic performance index with balanced factors."""
        # Normalization ranges
        min_cost, max_cost = 50, 500
        min_lead_time, max_lead_time = 1, 7
        min_value, max_value = 1, 5  # For uncertainty, sustainability, risk

        # Normalize all factors to 0 - 1
        total_cost_norm = (total_cost - min_cost) / (max_cost - min_cost)
        lead_time_norm = (lead_time - min_lead_time) / (max_lead_time - min_lead_time)
        demand_uncertainty_norm = (demand_uncertainty - min_value) / (max_value - min_value)
        risk_factor_norm = (risk_factor - min_value) / (max_value - min_value)
        sustainability_factor_norm = (sustainability_factor - min_value) / (max_value - min_value)

        # Ensure normalized values are between 0 and 1
        total_cost_norm = min(max(total_cost_norm, 0), 1)
        lead_time_norm = min(max(lead_time_norm, 0), 1)
        demand_uncertainty_norm = min(max(demand_uncertainty_norm, 0), 1)
        risk_factor_norm = min(max(risk_factor_norm, 0), 1)
        sustainability_factor_norm = min(max(sustainability_factor_norm, 0), 1)

        # Responsiveness factor is already between 0.1 and 1
        responsiveness_factor = min(max(responsiveness_factor, 0.1), 1)

        # Invert negative factors
        total_cost_inv = 1 - total_cost_norm
        lead_time_inv = 1 - lead_time_norm
        demand_uncertainty_inv = 1 - demand_uncertainty_norm
        risk_factor_inv = 1 - risk_factor_norm

        # Calculate weighted average
        index = (
            weights['cost'] * total_cost_inv +
            weights['lead_time'] * lead_time_inv +
            weights['demand_uncertainty'] * demand_uncertainty_inv +
            weights['risk_factor'] * risk_factor_inv +
            weights['sustainability_factor'] * sustainability_factor_norm +
            weights['responsiveness_factor'] * responsiveness_factor
        )
        return index

    # Function to apply external challenges
    def apply_external_challenges(cost1, cost2, demand_uncertainty):
        if "Supply Chain Disruption" in external_challenges:
            cost1 *= 1.3
        if "Tech Failure" in external_challenges:
            cost2 *= 1.2
        if "Global Demand Shift" in external_challenges:
            demand_uncertainty *= 1.6
        return cost1, cost2, demand_uncertainty

    # Function to create charts
    def create_chart(chart_type, labels, values, title):
        fig = go.Figure()
        if chart_type == "Bar Chart":
            fig.add_trace(go.Bar(x=labels, y=values, marker_color=['royalblue',
                            'forestgreen']))
        elif chart_type == "Pie Chart":
            fig.add_trace(go.Pie(labels=labels, values=values, hole=.3))
        elif chart_type == "Line Chart":
            fig.add_trace(go.Scatter(x=labels, y=values,
                                     mode='lines+markers',
                                     line=dict(color='purple', width=4)))
        fig.update_layout(title=title, yaxis_title="Million $",
                          xaxis_title="Cost Type",
                          legend_title="Cost Type", template="plotly_white")
        return fig

    # Title and description
    st.title("Advanced Supply Chain Strategy Simulation")
    st.subheader("Strategic Fit & Responsiveness Analysis")

    # Sidebar: User guide with tooltips
    st.sidebar.header("User Guide")
    st.sidebar.write("""
    **Instructions:**

    1. **Select a company** from the dropdown menu.
    2. **Adjust the sliders** for various costs and factors. Hover over the info icons for explanations.
    3. **Choose external challenges** that may affect performance.
    4. **Set a target performance index.**
    5. **Analyze the results** and adjust parameters as needed.
    6. **Answer the assignment questions** provided in the main area.
    7. **Download the simulation report** for submission.
    """)

    # Company selection
    company = st.sidebar.selectbox("Select Company",
                                   ("Netflix", "IKEA", "Amazon", "Wayfair"),
                                   help="Choose the company to simulate.")

    # Shared parameters (Demand Uncertainty, External Challenges)
    st.sidebar.header("Global Scenarios & Demand")
    demand_uncertainty = st.sidebar.slider("Implied Demand Uncertainty",
                                           min_value=1, max_value=5, value=3,
                                           help=(
                                               "Represents the variability in customer demand. "
                                               "A lower value indicates high uncertainty, "
                                               "while a higher value indicates low uncertainty."
                                           ))
    external_challenges = st.sidebar.multiselect("Select External Challenges",
        ["Supply Chain Disruption", "Tech Failure", "Global Demand Shift"],
        help="Select any external challenges affecting the supply chain.")

    # Additional factors with tooltips
    sustainability_factor = st.sidebar.slider("Sustainability Factor",
                                              min_value=1, max_value=5, value=3,
                                              help="Higher value indicates better sustainability practices.")
    risk_factor = st.sidebar.slider("Risk Factor", min_value=1, max_value=5, value=3,
                                    help="Higher value indicates higher risk.")

    # Weights adjustment (Advanced users)
    st.sidebar.header("Advanced Settings")
    adjust_weights = st.sidebar.checkbox("Adjust Performance Index Weights",
                                         help="Check to customize the weights for each factor.")

    # Default weights
    default_weights = {
        'cost': 0.2,
        'lead_time': 0.2,
        'demand_uncertainty': 0.2,
        'risk_factor': 0.1,
        'sustainability_factor': 0.2,
        'responsiveness_factor': 0.1
    }

    # Allow users to adjust weights if selected
    if adjust_weights:
        st.sidebar.subheader("Adjust Weights (Must sum to 1)")
        total_weight = 0
        weights = {}
        for key in default_weights.keys():
            weight = st.sidebar.number_input(f"Weight for {key.replace('_', ' ').title()}",
                                             min_value=0.0, max_value=1.0,
                                             value=default_weights[key], step=0.05)
            weights[key] = weight
            total_weight += weight

        if abs(total_weight - 1.0) > 0.01:
            st.sidebar.error("Weights must sum to 1. Please adjust.")
            st.stop()
    else:
        weights = default_weights

    # Company-specific parameters and analysis
    if company == "Amazon":
        st.header("Amazon: Fast Delivery & E-Commerce")
        cost_label1 = "Warehouse Operating Cost"
        cost_label2 = "Delivery Cost"
        cost1 = st.slider(f"{cost_label1} (Million $)", 50, 500, 250,
                          help="Cost associated with operating warehouses.")
        cost2 = st.slider(f"{cost_label2} (Million $)", 20, 300, 100,
                          help="Cost associated with delivering products to customers.")
        responsiveness_factor = 0.9  # Amazon prioritizes fast delivery

    elif company == "Netflix":
        st.header("Netflix: Digital Content & Global Distribution")
        cost_label1 = "Cloud Storage Cost"
        cost_label2 = "Content Production Cost"
        cost1 = st.slider(f"{cost_label1} (Million $)", 10, 100, 50,
                          help="Cost associated with cloud storage and streaming infrastructure.")
        cost2 = st.slider(f"{cost_label2} (Million $)", 50, 500, 150,
                          help="Cost of producing original content.")
        responsiveness_factor = 0.8  # Netflix is generally responsive

    elif company == "IKEA":
        st.header("IKEA: Flat-Pack Furniture & Global Retail")
        cost_label1 = "Manufacturing Cost"
        cost_label2 = "Transportation Cost"
        cost1 = st.slider(f"{cost_label1} (Million $)", 50, 500, 200,
                          help="Cost of manufacturing furniture.")
        cost2 = st.slider(f"{cost_label2} (Million $)", 20, 300, 80,
                          help="Cost of transporting goods globally.")
        responsiveness_factor = 0.6  # IKEA focuses on cost efficiency

    elif company == "Wayfair":
        st.header("Wayfair: Online Furniture Retailer")
        cost_label1 = "Warehouse Cost"
        cost_label2 = "Shipping Cost"
        cost1 = st.slider(f"{cost_label1} (Million $)", 50, 500, 150,
                          help="Cost of warehousing inventory.")
        cost2 = st.slider(f"{cost_label2} (Million $)", 30, 300, 90,
                          help="Cost of shipping products to customers.")
        responsiveness_factor = 0.5  # Wayfair balances cost and delivery

    # Apply external challenges
    cost1, cost2, demand_uncertainty = apply_external_challenges(cost1, cost2,
                                                                 demand_uncertainty)

    total_cost = cost1 + cost2
    lead_time = st.slider("Delivery Lead Time (Days)", 1, 7, 3,
                          help="Time taken to deliver products to customers.")

    # Calculate performance index without time factor
    performance_index = calculate_performance(
        total_cost, lead_time, demand_uncertainty, responsiveness_factor,
        sustainability_factor, risk_factor, weights)

    # Display results with detailed explanations
    st.subheader("Simulation Results")
    if performance_index is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{cost_label1}:** {cost1:.2f} Million $")
            st.write(f"**{cost_label2}:** {cost2:.2f} Million $")
            st.write(f"**Total Cost:** {total_cost:.2f} Million $")
            st.write(f"**Lead Time:** {lead_time} Days")
        with col2:
            st.write(f"**Responsiveness Factor:** {responsiveness_factor}")
            st.write(f"**Sustainability Factor:** {sustainability_factor}")
            st.write(f"**Risk Factor:** {risk_factor}")
            st.write(f"**Demand Uncertainty:** {demand_uncertainty}")
        st.write(f"**Performance Index (Strategic Fit & Responsiveness):** "
                 f"{performance_index:.2f}")

        # Show breakdown of performance index
        st.subheader("Performance Index Breakdown")
        index_components = {
            'Cost': weights['cost'] * (1 - (total_cost - 50) / (500 - 50)),
            'Lead Time': weights['lead_time'] * (1 - (lead_time - 1) / (7 - 1)),
            'Demand Uncertainty': weights['demand_uncertainty'] * (1 - (demand_uncertainty - 1) / (5 - 1)),
            'Risk Factor': weights['risk_factor'] * (1 - (risk_factor - 1) / (5 - 1)),
            'Sustainability': weights['sustainability_factor'] * ((sustainability_factor - 1) / (5 - 1)),
            'Responsiveness': weights['responsiveness_factor'] * responsiveness_factor
        }
        breakdown_df = pd.DataFrame(list(index_components.items()), columns=['Factor', 'Contribution'])
        st.table(breakdown_df)
    else:
        st.error("Performance Index could not be calculated. Please check your inputs.")

    # Chart type selection
    st.subheader("Cost Breakdown")
    chart_type = st.selectbox("Select Chart Type",
                              ("Bar Chart", "Pie Chart", "Line Chart"),
                              help="Choose how to visualize the cost breakdown.")
    fig = create_chart(chart_type, [cost_label1, cost_label2],
                       [cost1, cost2], f"{company} Cost Breakdown")
    st.plotly_chart(fig, use_container_width=True)

    # Challenge Mode: Goal is to achieve a target performance index
    st.sidebar.header("Challenge Mode")
    target_performance_index = st.sidebar.slider("Set Target Performance Index", 0.0, 1.0, 0.8,
                                                 help="Set your goal for the performance index.")

    # Check if performance_index has a value before accessing
    if performance_index is not None:
        st.sidebar.subheader("Challenge Outcome")
        st.sidebar.write(f"**Your Performance Index:** {performance_index:.2f}")
        st.sidebar.write(f"**Target Performance Index:** {target_performance_index:.2f}")

        if performance_index >= target_performance_index:
            st.sidebar.success("Congratulations! You have achieved the target performance index!")
        else:
            st.sidebar.warning("Try adjusting the values to reach the target.")
    else:
        st.sidebar.write("Please select a company and adjust the parameters to calculate the performance index.")

    # Educational content
    st.subheader("Learn More")
    with st.expander("Click here to expand and learn more about supply chain strategies."):
        st.write("""
        **Key Concepts:**

        - **Strategic Fit:** Aligning a company's supply chain strategy with its competitive strategy.
        - **Responsiveness:** The ability of a supply chain to respond purposefully and within an appropriate timeframe to customer requests or changes in the marketplace.
        - **Efficiency:** Operating at the lowest possible cost.

        **Trade-offs:**

        Companies often face trade-offs between responsiveness and efficiency. A highly responsive supply chain may incur higher costs, while a focus on efficiency might reduce responsiveness.

        **External Challenges:**

        Factors such as supply chain disruptions, technological failures, and global demand shifts can significantly impact supply chain performance.
        """)

    # Assignment Questions - Student Responses
    st.subheader("Assignment Questions")
    st.write("Please provide detailed answers to the following questions:")

    # List of assignment questions (excluding the last two)
    assignment_questions = [
        "1. How does the company adapt to global challenges in your simulation?",
        "2. What trade-offs did you observe between responsiveness and cost efficiency?",
        "3. How does demand uncertainty impact the company's ability to meet customer expectations?",
        "4. Compare the performance of two companies under the same external challenges. What strategies led to differences in their performance indices?",
        "5. Based on your simulation, what strategic changes would you recommend to improve the company's supply chain performance?",
        "6. How does the sustainability factor influence the performance index, and what does this imply for the company's strategic priorities?",
        "7. Identify potential risks in the supply chain and propose strategies to mitigate them.",
        "8. Evaluate how the company's supply chain strategy aligns with its overall business strategy.",
        "9. Discuss how technology can be leveraged to improve supply chain performance in the context of your simulation.",
        "10. Analyze the impact of global events on the company's supply chain and suggest ways to build resilience."
    ]

    # Collect responses
    responses = {}
    for i, question in enumerate(assignment_questions, 1):
        st.write(f"**{question}**")
        responses[f'Response Q{i}'] = st.text_area(f"Your Answer for Question {i}", "")

    # Collect data into a dictionary
    simulation_data = {
        'Company': company,
        'Cost Label 1': cost_label1,
        'Cost 1': cost1,
        'Cost Label 2': cost_label2,
        'Cost 2': cost2,
        'Total Cost': total_cost,
        'Lead Time': lead_time,
        'Responsiveness Factor': responsiveness_factor,
        'Sustainability Factor': sustainability_factor,
        'Risk Factor': risk_factor,
        'Demand Uncertainty': demand_uncertainty,
        'Performance Index': performance_index
    }

    # Combine simulation data and responses
    simulation_data.update(responses)

    # Generate text report
    def generate_text_report(data):
        report = ""
        report += "Supply Chain Strategy Simulation Report\n"
        report += "---------------------------------------\n\n"
        report += f"Company: {data['Company']}\n"
        report += f"{data['Cost Label 1']}: {data['Cost 1']:.2f} Million $\n"
        report += f"{data['Cost Label 2']}: {data['Cost 2']:.2f} Million $\n"
        report += f"Total Cost: {data['Total Cost']:.2f} Million $\n"
        report += f"Lead Time: {data['Lead Time']} Days\n"
        report += f"Responsiveness Factor: {data['Responsiveness Factor']}\n"
        report += f"Sustainability Factor: {data['Sustainability Factor']}\n"
        report += f"Risk Factor: {data['Risk Factor']}\n"
        report += f"Demand Uncertainty: {data['Demand Uncertainty']}\n"
        report += f"Performance Index: {data['Performance Index']:.2f}\n\n"

        report += "Assignment Responses:\n"
        report += "---------------------\n\n"
        for i, question in enumerate(assignment_questions, 1):
            response_key = f'Response Q{i}'
            report += f"{question}\n"
            report += f"{data[response_key]}\n\n"

        return report

    text_report = generate_text_report(simulation_data)

    # Add a download button for the text report
    st.download_button(
        label="Download Simulation Report",
        data=text_report,
        file_name='simulation_report.txt',
        mime='text/plain',
        help="Click to download your simulation data and assignment responses."
    )

    # Footer with additional resources
    st.markdown("---")
    st.write("For more information on supply chain management, check out the following resources:")
    st.write("- [Supply Chain Management by Sunil Chopra](https://www.pearson.com/us/higher-education/program/Chopra-Supply-Chain-Management-Strategy-Planning-and-Operation-7th-Edition/PGM333968.html)")
    st.write("- [MIT Center for Transportation & Logistics](https://ctl.mit.edu/)")
    st.write("- [Council of Supply Chain Management Professionals](https://cscmp.org/)")

    st.info("Created by Çiğdem Sıcakyüz (10/10/2024)")

if __name__ == "__main__":
    main()
