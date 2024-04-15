import MainView from "@/components/main";
import Head from 'next/head';
import { Inter } from 'next/font/google';

// Configuración de la fuente Inter optimizada para mejor rendimiento
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  weight: ["400", "700"]  // Especifica los pesos de fuente que se utilizarán
});

export default function Home() {
  return (
    <>
      <Head>
        <title>Projectile Trajectory Simulator</title>
        <meta name="description" content="Visualize the trajectory of a projectile in 3D using React and Three.js." />
      </Head>
      <MainView />
    </>
  );
}
