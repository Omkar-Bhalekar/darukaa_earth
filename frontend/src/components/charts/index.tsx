import React from 'react';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend, Filler
);

ChartJS.defaults.font.family = 'Inter';
ChartJS.defaults.color = '#2D3436';

export const LineChart: React.FC<React.ComponentProps<typeof Line>> = (props) => <Line {...props} />;
export const BarChart: React.FC<React.ComponentProps<typeof Bar>> = (props) => <Bar {...props} />;
export const DonutChart: React.FC<React.ComponentProps<typeof Doughnut>> = (props) => <Doughnut {...props} />;
