interface AssetStatus {
  liquidity: number;
  holders: number;
  contractAgeDays: number;
  activeWallets: number;
  networkRisk: number;
}

function assessAssetHealth(status: AssetStatus): string {
  const liquidityScore = Math.log(status.liquidity + 1);
  const holderScore = Math.sqrt(status.holders);
  const ageScore = status.contractAgeDays > 30 ? 2 : 0.5;
  const activeScore = status.activeWallets / 100;
  const riskPenalty = status.networkRisk;

  const healthScore = liquidityScore + holderScore + ageScore + activeScore - riskPenalty;

  if (healthScore > 15) return "✅ High Asset Health";
  if (healthScore > 10) return "🟡 Moderate Health";
  return "⚠️ Low Health";
}

const assets: AssetStatus[] = [];

for (let i = 0; i < 80; i++) {
  assets.push({
    liquidity: Math.random() * 100000,
    holders: Math.floor(Math.random() * 10000),
    contractAgeDays: Math.floor(Math.random() * 90),
    activeWallets: Math.floor(Math.random() * 1000),
    networkRisk: Math.random() * 5,
  });
}

assets.forEach((asset, i) => {
  console.log(`Asset #${i}:`, assessAssetHealth(asset));
});