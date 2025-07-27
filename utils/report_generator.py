import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import tempfile
import os
from zipfile import ZipFile
from io import BytesIO

def generate_interactive_report(df: pd.DataFrame, output_path="toxicity_report.html"):
    figs = []

    if 'TOXICITY' in df.columns:
        figs.append(px.histogram(df, x='TOXICITY', nbins=20, title='Toxicity Score Distribution'))

    attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'INSULT', 'THREAT', 'IDENTITY_ATTACK']
    cols = [col for col in attributes if col in df.columns]

    if cols:
        melted = df[cols].melt(var_name='Category', value_name='Score')
        figs.append(px.box(melted, x='Category', y='Score', title='Boxplot of Toxicity Categories'))

        if len(cols) >= 2:
            corr = df[cols].corr().round(2)
            heatmap = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale='Viridis',
                zmin=0,
                zmax=1,
                hoverongaps=False
            ))
            heatmap.update_layout(title='Correlation Heatmap')
            figs.append(heatmap)

    html_sections = []
    for fig in figs:
        html_sections.append(pio.to_html(fig, include_plotlyjs='cdn', full_html=False))

    html = "<html><head><title>Toxicity Report</title></head><body>" + "".join(html_sections) + "</body></html>"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

def generate_report_zip(df: pd.DataFrame) -> bytes:
    with tempfile.TemporaryDirectory() as temp_dir:
        excel_path = os.path.join(temp_dir, "toxicity_output.xlsx")
        html_path = os.path.join(temp_dir, "toxicity_report.html")
        zip_path = os.path.join(temp_dir, "toxicity_results.zip")

        df.to_excel(excel_path, index=False)
        generate_interactive_report(df, html_path)

        with ZipFile(zip_path, 'w') as zipf:
            zipf.write(excel_path, arcname="toxicity_output.xlsx")
            zipf.write(html_path, arcname="toxicity_report.html")

        with open(zip_path, 'rb') as f:
            return f.read()