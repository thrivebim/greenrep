import streamlit as st
import plotly_express as px
import plotly.io as pio
import pandas as pd
from fpdf import FPDF
import base64

pio.templates.default = 'plotly'

st.set_page_config(
        page_title="BREEAM International 2021",
        page_icon="leaves",
        layout="wide",
    )

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

with st.sidebar: st.caption(""":darkgrey[App made by car]""")
st.subheader("BREEAM International - 2021 Version")
st.write("Scroll through each section of the certification checklist and then check the score in the Rating tab")

tab1, tab2, tab3 = st.tabs(["Checklist","Rating","Print Output"])


@st.cache_data
def get_user_choices():
    return {building_proj: None, building_type: None, man_01_01: None, man_01_02: None, man_01_03: None, man_01_04: None }

with tab1:

    col1, col2 = st.columns ([1,3])

    with col1:
        building_proj = st.selectbox(("What type of project is?"),("Fully Fitted","Fully Fitted - Res Only","Shell and Core","Shell Only","Partially Fitted - Res Only"))

        building_type = st.selectbox(("What type of building is?"),("Non Residential","Single Res","Multi Res"))

    with col2:
        with st.container (height=400):

            st.write("Management Section")
            with st.expander("Man 01 - Project Brief and Design"):
                st.caption("4 credit maximum - No minimum standards")
                man_01_01 = st.number_input('Stakeholder Consultation - Project delivery',0,1)
                man_01_02 = st.number_input('Stakeholder Consultation - Third party',0,1)
                man_01_03 = st.number_input('Sustainability Champion - Design',0,1)
                man_01_04 = st.number_input('Sustainability Champion - Monitoring',0,1)
                man_01 = man_01_01 + man_01_02 + man_01_03 + man_01_04
                st.caption(f"Total Credit for this section is {man_01}")

            with st.expander("Man 02 - Life Cycle Cost and service life planning"):
                st.caption("4 credit maximum - No minimum standards")
                man_02_01 = st.number_input('Elemental Life Cycle Cost - ELCC',0,2)
                man_02_02 = st.number_input('Component LCC Options Appraisal',0,1)
                man_02_03 = st.number_input('Capital Cost Reporting',0,1)
                man_02 = man_02_01 + man_02_02 + man_02_03
                st.caption(f"Total Credit for this section is {man_02}")

            with st.expander("Man 03 - Responsible Construction Practice"):
                st.caption("6 credit maximum - Minimum Standards")
                man_03_01 = st.number_input('Environmental Management',0,1)
                man_03_02 = st.number_input('Sustainability Champion',0,1)
                man_03_03 = st.number_input('Considerate Construction',0,2)
                man_03_04 = st.number_input('Monitoring of Site impacts',0,2)
                man_03 = man_03_01 + man_03_02 + man_03_03 + man_03_04
                st.caption(f"Total Credit for this section is {man_03}")

            with st.expander("Man 04 - Commissioning and Handover"):
                st.caption("4 credit maximum - Minimum Standards")
                man_04_01 = st.number_input('Commissioning and testing schedule and responsibilities',0,1)
                man_04_02 = st.number_input('Commissioning building services',0,1)
                man_04_03 = st.number_input('Testing and inspecting building fabric',0,1)
                man_04_04 = st.number_input('Handover',0,1)
                man_04 = man_04_01 + man_04_02 + man_04_03 + man_04_04
                st.caption(f"Total Credit for this section is {man_04}")

            with st.expander("Man 05 - Aftercare"):
                st.caption("3 credit maximum - Minimum Standards")
                man_05_01 = st.number_input('Aftercare support',0,1)
                man_05_02 = st.number_input('Seasonal commissioning',0,1)
                man_05_03 = st.number_input('Post-occupancy evaluation',0,1)
                man_05 = man_05_01 + man_05_02 + man_05_03
                st.caption(f"Total Credit for this section is {man_05}")

            man_total= (man_01 + man_02 + man_03 + man_04 + man_05) / 21 *100

            if building_proj == ('Shell Only') and building_type == ('Non Residential'): man_perc = man_total * 0.1113
            elif building_proj == ('Shell and Core') and building_type == ('Non Residential'): man_perc = man_total * 0.1064
            elif building_proj == ('Fully Fitted') and building_type == ('Non Residential'): man_perc = man_total * 0.11
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Single Res'): man_perc = man_total * 0.091
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Multi Res'): man_perc = man_total * 0.1057
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Single Res'): man_perc = man_total * 0.0958
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Multi Res'): man_perc = man_total * 0.1118

            st.divider()

            st.write("Health and Wellbeing")

            with st.expander("Hea 01 - Visual Comfort"):
                st.caption("6 credit maximum - Minimum Standards crit 1 only")
                hea_01_00 = st.checkbox("Prerequisite")
                if hea_01_00 == True:
                    hea_01_01 = st.number_input('Glare control',0,1)
                    hea_01_02 = st.number_input('Daylighting',0,4)
                    hea_01_03 = st.number_input('View Out',0,1)
                    hea_01_04 = st.number_input('Internal and External Lighting',0,1)
                    hea_01 = hea_01_01 + hea_01_02 + hea_01_03 + hea_01_04
                    st.caption(f"Total Credit for this section is {hea_01}")
                else: hea_01 = 0

            with st.expander("Hea 02 - Indoor Quality"):
                st.caption("Up to 5 credit - Minimum Standards")
                hea_02_00 = st.checkbox("Prerequisite - Avoidance of Asbestos")
                if hea_02_00 == True:
                    hea_02_01 = st.number_input('Minimising sources of air pollution - 4 depending on building types',0,4)
                    hea_02_02 = st.number_input('Adaptability - potential for natural ventilation - 4 depending on building types',0,4)
                    hea_02 = hea_02_01 + hea_02_02
                    st.caption(f"Total Credit for this section is {hea_02}")
                else: hea_02 = 0

            with st.expander("Hea 03 - Safe Containment in laboratories"):
                st.caption("2 credit maximum - For Science Projects Only")
                hea_03_01 = st.number_input('Laboratory containment devices and containment areas',0,1)
                hea_03_02 = st.number_input('Buildings with containment level 2 and 3 laboratory facilities',0,1)
                hea_03 = hea_03_01 + hea_03_02
                st.caption(f"Total Credit for this section is {hea_03}")

            with st.expander("Hea 04 - Thermal Comfort"):
                st.caption("3 credit maximum")
                hea_04_01 = st.number_input('Thermal Modeling',0,1)
                hea_04_02 = st.number_input('Adaptability for a projected climate change scenario',0,1)
                hea_04_03 = st.number_input('Thermal zoning and controls',0,1)
                hea_04 = hea_04_01 + hea_04_02 + hea_04_03
                st.caption(f"Total Credit for this section is {hea_04}")

            with st.expander("Hea 05 - Acoustic Performance"):
                st.caption("Up to 4 credit")
                hea_05_00 = st.checkbox('Prerequisite - Acoustic Professional')
                if hea_05_00 == True:
                    hea_05_01 = st.number_input('Acoustic performance standards - up to 4',0,4)
                    hea_05 = hea_05_01
                    st.caption(f"Total Credit for this section is {hea_05}")
                else: hea_05 = 0

            with st.expander("Hea 06 - Accessibility"):
                st.caption("2 credits - 3 credits for Residential - Minimum (Residentials)")
                hea_06_01 = st.number_input('Safe Access',0,1)
                hea_06_02 = st.number_input('Inclusive and accessible design - Not for Residential',0,1)
                hea_06_03 = st.number_input('Inclusive and accessible design - Residential only',0,2)
                hea_06 = hea_06_01 + hea_06_02 + hea_06_03
                st.caption(f"Total Credit for this section is {hea_06}")

            with st.expander("Hea 07 - Hazards"):
                st.caption("1 credit")
                hea_07_01 = st.number_input('Risk Assessment',0,1)
                hea_07 = hea_07_01
                st.caption(f"Total Credit for this section is {hea_07}")


            with st.expander("Hea 08 - Private Space - For Residential Only"):
                st.caption("1 credit - Minimum requirements")
                hea_08_01 = st.number_input('Private Space',0,1)
                hea_08 = hea_08_01
                st.caption(f"Total Credit for this section is {hea_08}")


            with st.expander("Hea 09 - Water Quality"):
                st.caption("1 credits - Minimum requirements - Criterion 1")
                hea_09_01 = st.number_input('Water quality requirements for Building Services and Occupants',0,1)
                hea_09 = hea_09_01
                st.caption(f"Total Credit for this section is {hea_09}")

            hea = (hea_01 + hea_02 + hea_03 + hea_04 + hea_05 + hea_06 + hea_07 + hea_08 + hea_09) / 21 *100

            if building_proj == ('Shell Only') and building_type == ('Non Residential'): hea_perc = hea * 0.1266
            elif building_proj == ('Shell and Core') and building_type == ('Non Residential'): hea_perc = hea * 0.1387
            elif building_proj == ('Fully Fitted') and building_type == ('Non Residential'): hea_perc = hea * 0.19
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Single Res'): hea_perc = hea * 0.2170
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Multi Res'): hea_perc = hea * 0.2149
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Single Res'): hea_perc = hea * 0.2164
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Multi Res'): hea_perc = hea * 0.2170

            st.divider()

            st.write("Energy")

            with st.expander("Ene 01 - Reduction of energy use and carbon emissions"):
                st.caption("13 credits - Minimum requirements")
                ene_01_01 = st.number_input('Energy Performance - EPR - No NCM, up to 9 credits',0,9)
                ene_01_02 = st.number_input('Prediction of operational energy consumption',0,4)
                ene_01 = ene_01_01 + ene_01_02
                st.caption(f"Total Credit for this section is {ene_01}")

            with st.expander("Ene 02a - Energy Monitoring"):
                st.caption("2 credits - Minimum Requirements - For Non residential and residential institutions only")
                ene_02a_01 = st.number_input('Sub Metering by end-use',0,1)
                ene_02a_02 = st.number_input('Sub Metering by functional or tenanted areas',0,1)
                st.caption("Note: this credit does not apply for preschools, primary schools and residential institutions")
                ene_02a = ene_02a_01 + ene_02a_02
                st.caption(f"Total Credit for this section is {ene_02a}")

            with st.expander("Ene 02b - Energy Monitoring"):
                st.caption("2 credits - Residential only")
                ene_02b_01 = st.number_input('Current and/or primary power fuel consumption are displayed to the occupants',0,2)
                ene_02b = ene_02b_01
                st.caption(f"Total Credit for this section is {ene_02b}")

            with st.expander("Ene 03 - External Lighting"):
                st.caption("1 credit")
                ene_03_01 = st.number_input('External lighting requirements for BREEAM are met',0,1)
                ene_03 = ene_03_01
                st.caption(f"Total Credit for this section is {ene_03}")

            with st.expander("Ene 04 - Low Carbon Design"):
                st.caption("3 credits")
                ene_04_01 = st.number_input('Passive design',0,2)
                ene_04_02 = st.number_input('Low or Zero carbon technologies',0,1)
                ene_04 = ene_04_01 + ene_04_02
                st.caption(f"Total Credit for this section is {ene_04}")

            with st.expander("Ene 05 - Energy Efficient Cold Storage"):
                st.caption("3 credits - Non residential only")
                ene_05_01 = st.number_input('Energy efficient design, installation and commissioning',0,1)
                ene_05_02 = st.number_input('Energy efficient criteria',0,1)
                ene_05_03 = st.number_input('Reducing lifetime greenhouses gas emissions from energy use',0,1)
                ene_05 = ene_05_01 + ene_05_02 + ene_05_03
                st.caption(f"Total Credit for this section is {ene_05}")

            with st.expander("Ene 06 - Energy Efficient Transport Systems"):
                st.caption("3 credits - All buildings")
                ene_06_01 = st.number_input('Energy consumption',0,1)
                ene_06_02 = st.number_input('Energy Efficient features',0,2)
                ene_06 = ene_06_01 + ene_06_02
                st.caption(f"Total Credit for this section is {ene_06}")

            with st.expander("Ene 07 - Energy Efficient Laboratory Systems"):
                st.caption("1 to 5 credits - non residential only")
                ene_07_00 = st.checkbox('Prerequisite - Hea 03 - Safe containment in laboratories - is achieved?')
                if ene_07_00 == True :
                    ene_07_01 = st.number_input('Design Specification',0,1)
                    ene_07_02 = st.number_input('Best practices for energy efficient measures',0,4)
                    ene_07 = ene_07_01 + ene_07_02
                    st.caption(f"Total Credit for this section is {ene_07}")
                else: ene_07 = 0

            with st.expander("Ene 08 - Energy Efficient Equipment"):
                st.caption("2 credits - all buildings")
                ene_08_01 = st.number_input('Equipment consuption reduction strategies effective',0,2)
                ene_08 = ene_08_01
                st.caption(f"Total Credit for this section is {ene_08}")

            with st.expander("Ene 09 - Drying Space"):
                st.caption("not available credits")
                ene_09_01 = st.number_input('not available in the current version, please wait for further updates on SD',0,0)
                ene_09 = ene_09_01
                st.caption(f"Total Credit for this section is {ene_09}")

            with st.expander("Ene 10 - Flexible Demand Side Response"):
                st.caption("1 exemplary credit - check Innovation section for calculation")
                ene_10_01 = st.number_input('Demand Response strategy for the project mets the requirements',0,0)
                ene_10 = ene_10_01
                st.caption(f"Total Credit for this section is {ene_10}")

            ene = (ene_01 + ene_02a + ene_02b + ene_03 + ene_04 + ene_05 + ene_06 + ene_07 + ene_08 + ene_09 + ene_10) / 32 *100
            
            if building_proj == ('Shell Only') and building_type == ('Non Residential'): ene_perc = ene * 0.2007
            elif building_proj == ('Shell and Core') and building_type == ('Non Residential'): ene_perc = ene * 0.1909
            elif building_proj == ('Fully Fitted') and building_type == ('Non Residential'): ene_perc = ene * 0.20
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Single Res'): ene_perc = ene * 0.2123
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Multi Res'): ene_perc = ene * 0.1997
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Single Res'): ene_perc = ene * 0.1903
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Multi Res'): ene_perc = ene * 0.1798

            st.divider()

            st.write("Transport")

            with st.expander("Tra 01 - Public Transport Accessibility"):
                st.caption("up to 5 credits - Building Type dependent")
                tra_01_01 = st.number_input('Bus Services',0,1)
                tra_01_02 = st.number_input('Accessibility index - Please consult BREEAM guidance for specific building type goals',0,5)
                tra_01 = tra_01_01 + tra_01_02
                st.caption(f"Total Credit for this section is {tra_01}")

            with st.expander("Tra 02 - Proximity to Amenities"):
                st.caption("Up to 2 credits - Building type dependant")
                tra_02_01 = st.number_input('',0,1)
                tra_02 = tra_02_01
                st.caption(f"Total Credit for this section is {tra_02}")

            with st.expander("Tra 03a - Alternative methods of transport"):
                st.caption("2 credits - non residential and residential institutions")
                tra_03a_01 = st.number_input('Alternative methods - comply with one criteria',0,2)
                tra_03a = tra_03a_01
                st.caption(f"Total Credit for this section is {tra_03a}")

            with st.expander("Tra 03b - Alternative methods of transport"):
                st.caption("2 credits - only residential")
                tra_03b_01 = st.number_input('Alternative methods - comply with one criteria for residential',0,2)
                tra_03b = tra_03b_01
                st.caption(f"Total Credit for this section is {tra_03b}")

            with st.expander("Tra 04 - Maximum car parking capacity"):
                st.caption("2 credits - non residential and residential institutions")
                tra_04_01 = st.number_input('Car parking capacity, based on building type',0,2)
                tra_04 = tra_04_01
                st.caption(f"Total Credit for this section is {tra_04}")

            with st.expander("Tra 05 - Travel Plan"):
                st.caption("1 credit - non residential, residential institutions and multi-dwelling only")
                tra_05_01 = st.number_input('The building is under or promotes a travel plan',0,1)
                tra_05 = tra_05_01
                st.caption(f"Total Credit for this section is {tra_05}")

            with st.expander("Tra 06 - Home office"):
                st.caption("1 credit - Residential only")
                tra_06_01 = st.number_input('Home office are integrated in the design',0,1)
                tra_06 = ene_06_01
                st.caption(f"Total Credit for this section is {tra_06}")

            tra= (tra_01 + tra_02 + tra_03a + tra_03b + tra_04 + tra_05 + tra_06) / 11 *100

            if building_proj == ('Shell Only') and building_type == ('Non Residential'): tra_perc = tra * 0.0850
            elif building_proj == ('Shell and Core') and building_type == ('Non Residential'): tra_perc = tra * 0.0677
            elif building_proj == ('Fully Fitted') and building_type == ('Non Residential'): tra_perc = tra * 0.06
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Single Res'): tra_perc = tra * 0.0613
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Multi Res'): tra_perc = tra * 0.0641
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Single Res'): tra_perc = tra * 0.0574
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Multi Res'): tra_perc = tra * 0.0610

            st.divider()

            st.write("Water")

            with st.expander("Wat 01 - Water Consumption"):
                st.caption("5 credits")
                wat_01_01 = st.number_input('Credit based on water consumption reduction percentage achieved',0,5)
                wat_01 = wat_01_01
                st.caption(f"Total Credit for this section is {wat_01}")

            with st.expander("Wat 02 - Water Monitoring"):
                st.caption("1 credit - Minimum standards")
                wat_02_01 = st.number_input('Water monitoring requirements met',0,1)
                wat_02 = wat_02_01
                st.caption(f"Total Credit for this section is {wat_02}")

            with st.expander("Wat 03 - Water Leak Detection and Prevention"):
                st.caption("2 credits - Building type dependant")
                wat_03_01 = st.number_input('Leak detection system',0,1)
                wat_03_02 = st.number_input('Flow control device - not for residential',0,1)
                wat_03_03 = st.number_input('Leak isolation - residential only',0,1)
                wat_03 = wat_03_01 + wat_03_02 + wat_03_03
                st.caption(f"Total Credit for this section is {wat_03}")

            with st.expander("Wat 04 - Water Efficient Systems"):
                st.caption("1 credit")
                wat_04_01 = st.number_input('Water Efficient Equipment equipped',0,1)
                wat_04 = wat_04_01
                st.caption(f"Total Credit for this section is {wat_04}")

            wat = (wat_01 + wat_02 + wat_03 + wat_04) / 9 *100

            if building_proj == ('Shell Only') and building_type == ('Non Residential'): wat_perc = wat * 0.0330
            elif building_proj == ('Shell and Core') and building_type == ('Non Residential'): wat_perc = wat * 0.0790
            elif building_proj == ('Fully Fitted') and building_type == ('Non Residential'): wat_perc = wat * 0.07
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Single Res'): wat_perc = wat * 0.0636
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Multi Res'): wat_perc = wat * 0.0673
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Single Res'): wat_perc = wat * 0.0669
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Multi Res'): wat_perc = wat * 0.0632

            st.write("Materials")

            with st.expander("Mat 01 - Life Cycle Impact"):
                st.caption("1 to 6 credits - Building Type dependent")
                mat_01_01 = st.number_input('BREAM calculator point',0,5)
                mat_01_02 = st.number_input('Environmental Product Declarations',0,5)
                mat_01_03 = st.number_input('Exemplary performance, see Innovation section',0,0)
                mat_01 = mat_01_01 + mat_01_02
                st.caption(f"Total Credit for this section is {mat_01}")

            with st.expander("Mat 02 - Hard landscaping and boundary protection"):
                st.caption("Not assessed on BREAAM international, but integrated as part of Mat 01")

            with st.expander("Mat 03 - Responsible sourcing of construction products"):
                st.caption("4 credits - Criterion 1 required")
                mat_03_00 = st.checkbox('Prerequisite - Legally harvested timber products')
                if mat_03_00 == True:
                    mat_03_01 = st.number_input('Sustainable procurement plan',0,1)
                    mat_03_02 = st.number_input('Responsible sourcing of construction products',0,4)
                    mat_03_03 = st.number_input('Exemplary performance, please check in the Innovation section',0,0)
                    mat_03 = mat_03_01 + mat_03_02
                    st.caption(f"Total Credit for this section is {mat_03}")
                else: mat_03 = 0

            with st.expander("Mat 04 - Insulation"):
                st.caption("Not assessed on BREEAM International, but integrated with Mat 01")

            with st.expander("Mat 05 - Designing for durability and resilience"):
                st.caption("1 credit")
                mat_05_01 = st.number_input('Design Durability principles met',0,1)
                mat_05 = mat_05_01
                st.caption(f"Total Credit for this section is {mat_05}")

            with st.expander("Mat 06 - Material Efficiency"):
                st.caption("1 credit")
                mat_06_01 = st.number_input('Material efficiency assessment during stages',0,1)
                mat_06 = mat_06_01
                st.caption(f"Total Credit for this section is {mat_06}")

            mat = (mat_01 + mat_03 + mat_05 + mat_06) / 12 *100

            if building_proj == ('Shell Only') and building_type == ('Non Residential'): mat_perc = mat * 0.1467
            elif building_proj == ('Shell and Core') and building_type == ('Non Residential'): mat_perc = mat * 0.1841
            elif building_proj == ('Fully Fitted') and building_type == ('Non Residential'): mat_perc = wat * 0.13
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Single Res'): mat_perc = wat * 0.1398
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Single Res'): mat_perc = wat * 0.1329
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Multi Res'): mat_perc = wat * 0.1321
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Multi Res'): mat_perc = wat * 0.1250
            
            st.divider()

            st.write("Waste")

            with st.expander("Wst 01 - Construction Waste Management"):
                st.caption("3 credit - all buildings - Minimum standards")
                wst_01_01 = st.number_input('Construction waste reduction',0,2)
                wst_01_02 = st.number_input('Diversion of resources from landfill',0,1)
                wst_01_03 = st.number_input('Exemplary credit, please look in the innovation section',0,0)
                wst_01 = wst_01_01 + wst_01_02
                st.caption(f"Total Credit for this section is {wst_01}")

            with st.expander("Wst 02 - Recycled Aggregates"):
                st.caption("1 credit - All buildings")
                wst_02_01 = st.number_input('Recycled aggregates',0,1)
                wst_02_02 = st.number_input('Exemplary credit, please look in the innovation section for Wst 02',0,0)
                wst_02 = wst_02_01
                st.caption(f"Total Credit for this section is {wst_02}")

            with st.expander("Wst 03a - Operational Waste"):
                st.caption("1 credit - Minimum standards - non residential and residential instituions")
                wst_03a_01 = st.number_input('Operational waste criterias are met',0,1)
                wst_03a = wst_03a_01
                st.caption(f"Total Credit for this section is {wst_03a}")

            with st.expander("Wst 03b - Operational Waste"):
                st.caption("2 credits - Minimum standards - for residential only")
                wst_03b_01 = st.number_input('Recycling',0,1)
                wst_03b_02 = st.number_input('Composting',0,1)
                wst_03b = wst_03b_01 + wst_03b_02
                st.caption(f"Total Credit for this section is {wst_03b}")

            with st.expander("Wst 04 - Speculative Finishes"):
                st.caption("1 credit")
                wst_04_01 = st.number_input('Speculative finishes',0,1)
                wst_04 = wst_04_01
                st.caption(f"Total Credit for this section is {wst_04}")

            with st.expander("Wst 05 - Adaptation to Climate Changes"):
                st.caption("1 credit")
                wst_05_01 = st.number_input('Adaptation to climate change - structural and fabric resilience',0,1)
                wst_05_02 = st.number_input('Exemplary credit, please look at Innovation section Wst 05 ',0,0)
                wst_05 = wst_05_01
                st.caption(f"Total Credit for this section is {wst_05}")

            with st.expander("Wst 06 - Functional Adaptability"):
                st.caption("1 credit - non residential only")
                wst_06_01 = st.number_input('Functional adaptability',0,1)
                wst_06 = wst_06_01
                st.caption(f"Total Credit for this section is {wst_06}")

            wst = (wst_01 + wst_02 + wst_03a + wst_03b + wst_04 + wst_05 + wst_06)  / 10 *100

            if building_proj == ('Shell Only') and building_type == ('Non Residential'): wst_perc = wst * 0.0743
            elif building_proj == ('Shell and Core') and building_type == ('Non Residential'): wst_perc = wst * 0.0677
            elif building_proj == ('Fully Fitted') and building_type == ('Non Residential'): wst_perc = wst * 0.060
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Single Res'): wst_perc = wst * 0.0565
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Single Res'): wst_perc = wst * 0.0537
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Multi Res'): wst_perc = wst * 0.061
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Multi Res'): wst_perc = wst * 0.0577

            st.divider()

            st.write("Land Use and Ecology")

            with st.expander("LE 01 - Site Selection"):
                st.caption("3 credit - all buildings")
                le_01_01 = st.number_input('Previously occupied land',0,2)
                le_01_02 = st.number_input('Contaminated Lands',0,1)
                le_01 = le_01_01 + le_01_02
                st.caption(f"Total Credit for this section is {le_01}")

            with st.expander("LE 02 - Ecological value of site and protection of ecological features"):
                st.caption("2 credit - all buildings")
                le_02_01 = st.number_input('Ecological value of site',0,1)
                le_02_02 = st.number_input('Protection of ecological features',0,1)
                le_02 = le_02_01 + le_02_02
                st.caption(f"Total Credit for this section is {le_02}")

            with st.expander("LE 03 - Minimising impact on existing site ecology"):
                st.caption("Credit not available in LEED international version 6")

            with st.expander("LE 04 - Enhancing Site Ecology"):
                st.caption("3 credits - all buildings")
                le_04_01 = st.number_input('Ecologist report reccomendations',0,1)
                le_04_02 = st.number_input('Increase in ecological value',0,2)
                le_04 = le_04_01 + le_04_02
                st.caption(f"Total Credit for this section is {le_04}")

            with st.expander("LE 05 - Long term impact on biodiversity"):
                st.caption("Up to 2 credits - all buildings")
                le_05_01 = st.number_input('Impact assessment',0,2)
                le_05 = le_05_01
                st.caption(f"Total Credit for this section is {le_05}")

            le_tot = (le_01 + le_02 + le_04 + le_05)  / 10 *100

            if building_proj == ('Shell Only') and building_type == ('Non Residential'): le_perc = le_tot * 0.0902
            elif building_proj == ('Shell and Core') and building_type == ('Non Residential'): le_perc = le_tot * 0.0902
            elif building_proj == ('Fully Fitted') and building_type == ('Non Residential'): le_perc = le_tot * 0.08
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Single Res'): le_perc = le_tot * 0.0860
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Single Res'): le_perc = le_tot * 0.0818
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Multi Res'): le_perc = le_tot * 0.0813
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Multi Res'): le_perc = le_tot * 0.0769

            st.write("Pollution")

            with st.expander("Pol 01 - Impact of refrigerants"):
                st.caption("up to 4 credits - all buildings")
                pol_01_01 = st.number_input('Ozone depleting potential - ODP',0,1)
                pol_01_02 = st.number_input('Impact of refrigerant or refrigerant leaks',0,2)
                pol_01_03 = st.number_input('Leak Detection',0,1)
                pol_01 = pol_01_01 + pol_01_02 + pol_01_03
                st.caption(f"Total Credit for this section is {pol_01}")

            with st.expander("Pol 02 - NOx Emissions"):
                st.caption("2 credit - all buildings")
                pol_02_01 = st.number_input('Emissions criterias met',0,2)
                pol_02 = pol_02_01
                st.caption(f"Total Credit for this section is {pol_02}")

            with st.expander("Pol 03 - Surface Water run-off"):
                st.caption("5 credits - all buildings")
                pol_03_01 = st.number_input('Flood risk',0,2)
                pol_03_02 = st.number_input('Surface water run-off',0,2)
                pol_03_03 = st.number_input('Minimising watercourse pollution',0,1)
                pol_03 = pol_03_01 + pol_03_02 + pol_03_03
                st.caption(f"Total Credit for this section is {pol_03}")

            with st.expander("Pol 04 - Reduction of night time light run-off"):
                st.caption("1 credit - non residential, residential institutions only")
                pol_04_01 = st.number_input('Reduction design strategies or operational strategies in place',0,1)
                pol_04 = pol_04_01
                st.caption(f"Total Credit for this section is {pol_04}")

            with st.expander("Pol 05 - Reduction of noise pollution"):
                st.caption("1 credit - non residential, residential instituions and multiple dwellings")
                pol_05_01 = st.number_input('Reduction noise pollution strategies satifies the requirements',0,1)
                pol_05 = pol_05_01
                st.caption(f"Total Credit for this section is {pol_05}")

            pol = (pol_01 + pol_02 + pol_03 + pol_04 + pol_05)  / 12 *100

            if building_proj == ('Shell Only') and building_type == ('Non Residential'): pol_perc = pol * 0.0654
            elif building_proj == ('Shell and Core') and building_type == ('Non Residential'): pol_perc = pol * 0.1228
            elif building_proj == ('Fully Fitted') and building_type == ('Non Residential'): pol_perc = pol * 0.10
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Single Res'): pol_perc = pol * 0.0910
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Single Res'): pol_perc = pol * 0.0865
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Multi Res'): pol_perc = pol * 0.0938
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Multi Res'): pol_perc = pol * 0.0887

            st.divider()

            st.write("Innovation")

            with st.expander("Innovation Credits"):
                st.caption("Up to 10 credits - on 12 available credits from other sections")
                ino_01 = st.number_input('Man 03 Responsible construction practices',0,1)
                ino_02 = st.number_input('Man 05 Aftercare',0,1)
                ino_03 = st.number_input('Hea 02 Indoor air quality',0,1)
                ino_04 = st.number_input('Ene 01 Reduction of energy use and carbon emissions',0,1)
                ino_05 = st.number_input('Ene 10 Flexible demand side response',0,1)
                ino_06 = st.number_input('Tra 03a Alternative modes of transport or Tra 03b Alternative modes of transport',0,1)
                ino_07 = st.number_input('Wat 01 Water consumption',0,1)
                ino_08 = st.number_input('Mat 01 Life cycle impacts',0,1)
                ino_09 = st.number_input('Mat 03 Responsible sourcing of construction products',0,1)
                ino_10 = st.number_input('Wst 01 Construction waste management',0,1)
                ino_11 = st.number_input('Wst 02 Recycled aggregates',0,1)
                ino_12 = st.number_input('Wst 05 Adaptation to climate change',0,1)
                ino = (ino_01 + ino_02 + ino_03 + ino_04 + ino_05 + ino_06 + ino_07 + ino_08 + ino_09 + ino_10 + ino_11 + ino_12)  *10
            
            if building_proj == ('Shell Only') and building_type == ('Non Residential'): ino_perc = ino * 0.10
            elif building_proj == ('Shell and Core') and building_type == ('Non Residential'): ino_perc = ino * 0.10
            elif building_proj == ('Fully Fitted') and building_type == ('Non Residential'): ino_perc = ino * 0.10
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Single Res'): ino_perc = ino * 0.10
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Single Res'): ino_perc = ino * 0.10
            elif building_proj == ('Partially Fitted - Res Only') and building_type == ('Multi Res'): ino_perc = ino * 0.10
            elif building_proj == ('Fully Fitted - Res Only') and building_type == ('Multi Res'): ino_perc = ino * 0.10

with tab2:
    col1,col2 = st.columns([2,5])

    with col1:
        rating = pd.DataFrame({"credit": ["Maintenance","Health", "Energy", "Transportation", "Water", "Material","Waste","Land Use","Pollution","Innovation"], "weight": [round(man_perc,2),round(hea_perc,2),round(ene_perc,2),round(tra_perc,2),round(wat_perc,2),round(mat_perc,2),round(wst_perc,2),round(le_perc,2),round(pol_perc,2),round(ino_perc,2)]})
        ratingdata = [["Maintenance", str(round(man_perc,2))],
    ["Health", str(round(hea_perc,2))],
    ["Energy", str(round(ene_perc,2))],
    ["Transportation", str(round(tra_perc,2))],
    ["Water", str(round(wat_perc,2))],
    ["Material", str(round(mat_perc,2))],
    ["Waste", str(round(wst_perc,2))],
    ["Land Use", str(round(le_perc,2))],
    ["Pollution", str(round(pol_perc,2))],
    ["Innovation", str(round(ino_perc,2))]]
        ratinglist = list(ratingdata)
        total = man_perc + hea_perc + ene_perc + tra_perc + wat_perc + mat_perc + wst_perc + le_perc + pol_perc + ino_perc
        credit = ["Maintenance","Health", "Energy", "Transportation", "Water", "Material","Waste","Land Use","Pollution","Innovation"]
        weight = [round(man_perc,2),round(hea_perc,2),round(ene_perc,2),round(tra_perc,2),round(wat_perc,2),round(mat_perc,2),round(wst_perc,2),round(le_perc,2),round(pol_perc,2),round(ino_perc,2)]
        totalround = round(total,2)
        if totalround < 30: rat = "Unclassified"
        elif totalround >= 30: rat = "Pass"
        elif totalround >= 45: rat = "Good"
        elif totalround >= 55: rat = "Very Good"
        elif totalround >= 70: rat = "Excellent"
        elif totalround >= 85: rat = "Outstanding"

        st.write(f'Total is {totalround}%')
        st.write(f'''The current Rating is **:green[{rat}]**''')
        st.caption(f"Maintenance: The percentage is {round(man_perc,2)}%")
        st.caption(f"Health and wellbeing: The percentage is {round(hea_perc,2)}%")
        st.caption(f"Energy: The percentage is {round(ene_perc,2)}%")
        st.caption(f"Transportation: The percentage is {round(tra_perc,2)}%")
        st.caption(f"Water: The percentage is {round(wat_perc,2)}%")
        st.caption(f"Materials: The percentage is {round(mat_perc,2)}%")
        st.caption(f"Waste: The percentage is {round(wst_perc,2)}%")
        st.caption(f"Land and ecology: The percentage is {round(le_perc,2)}%")
        st.caption(f"Pollution: The percentage is {round(pol_perc,2)}%")
        st.caption(f"Innovation: The percentage is {round(ino_perc,2)}%")

    with col2:
        chart = px.pie(rating, values='weight', names='credit',
             title='Split by Category',
             hover_data=['credit'], labels=[weight])
        chart.update_traces(textposition='inside', textinfo='percent+label',textfont_size=14) 
        st.plotly_chart(chart, theme='streamlit')
        chart.write_image('images/chart.jpg')

with tab3:
    col1,col2 = st.columns([2,5])

    with col1:
        project_input = st.text_input(
        "Enter the project name: ")
        type_input = st.text_input(
        "Enter the project type: ")
        nation_input = st.text_input(
        "Enter the project country: ")
        year_input = st.text_input(
        "Enter the rating year: ")
        st.divider()
        export_as_pdf = st.button("Export Report")

        def create_download_link(val, filename):
            b64 = base64.b64encode(val)  # val looks like b'...'
            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
        
        class PDF(FPDF):
            def header(self):
                self.image('greenb-icon.png',12,12,10)
                self.set_font('arial','B',10)
                self.cell(0,8,'Green Report App', border=False, ln=1, align='R')
                self.ln(12)

        if export_as_pdf:
            pdf = PDF('P','mm','A4')
            pdf.set_title(f'Green Report App - {project_input}')
            pdf.set_author('The Green B')
            pdf.set_auto_page_break(auto=True,margin=12)
            pdf.add_page()
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 12, f"Project Name: {project_input}", ln=1)
            pdf.cell(0, 12, f"Project Type: {type_input}", ln=1)
            pdf.cell(0, 12, f"Nation: {nation_input}", ln=1)
            pdf.cell(0, 12, f"Year of Certification: {year_input}", ln=1)
            pdf.ln(14)
            pdf.cell(60,12, txt="Maintenance",border=1)
            pdf.cell(30,12, txt=str(round(man_perc,2)),border=1, ln=1)
            pdf.cell(60,12, txt="Health and wellbeing",border=1)
            pdf.cell(30,12, txt=str(round(hea_perc,2)),border=1, ln=1)
            pdf.cell(60,12, txt="Energy",border=1)
            pdf.cell(30,12, txt=str(round(ene_perc,2)),border=1, ln=1)
            pdf.cell(60,12, txt="Transportation",border=1)
            pdf.cell(30,12, txt=str(round(tra_perc,2)),border=1, ln=1)
            pdf.cell(60,12, txt="Water",border=1)
            pdf.cell(30,12, txt=str(round(wat_perc,2)),border=1, ln=1)
            pdf.cell(60,12, txt="Materials",border=1)
            pdf.cell(30,12, txt=str(round(mat_perc,2)),border=1, ln=1)
            pdf.cell(60,12, txt="Waste",border=1)
            pdf.cell(30,12, txt=str(round(wst_perc,2)),border=1, ln=1)
            pdf.cell(60,12, txt="Land Use and Ecology",border=1)
            pdf.cell(30,12, txt=str(round(le_perc,2)),border=1, ln=1)
            pdf.cell(60,12, txt="Pollution",border=1)
            pdf.cell(30,12, txt=str(round(man_perc,2)),border=1, ln=1)
            pdf.cell(60,12, txt="Innovation",border=1)
            pdf.cell(30,12, txt=str(round(man_perc,2)),border=1, ln=1)
            pdf.ln(14)
            pdf.cell(0, 12,f"The total is {totalround}%",ln=1)
            pdf.cell(0, 12,f"Rating for this project could be {rat}",ln=1)
            pdf.add_page()
            pdf.image('images/chart.jpg',16,24,w=160)
        
            html = create_download_link(pdf.output(dest="S").encode("latin-1"), "reportpage")
            st.markdown(html, unsafe_allow_html=True)
    with col2:
        ""


