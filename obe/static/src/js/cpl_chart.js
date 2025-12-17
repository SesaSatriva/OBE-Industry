/** @odoo-module **/

import { Component, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class CPLChart extends Component {
    static template = "obe.CPLChart";

    setup() {
        this.canvasRef = useRef("canvas");

        onMounted(() => {
            const data = JSON.parse(this.props.chartData || "{}");
            if (!data.labels || !data.values) {
                return;
            }

            new Chart(this.canvasRef.el, {
                type: "bar",
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: "Ketercapaian CPL (%)",
                        data: data.values,
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                        },
                    },
                },
            });
        });
    }
}

registry.category("public_components").add(
    "obe.cpl_chart",
    CPLChart
);