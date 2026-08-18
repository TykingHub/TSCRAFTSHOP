const express = require("express");
const path = require("path");

const app = express();

const PORT = process.env.PORT || 3000;

// Permitir recibir JSON
app.use(express.json());

// Servir tu tienda
app.use(express.static(path.join(__dirname, "public")));

// Lista temporal de compras
let purchases = [];

// =========================
// RECIBIR COMPRA
// =========================

app.post("/api/purchases", (req, res) => {

    const purchase = req.body;

    if (!purchase) {
        return res.status(400).json({
            success: false,
            message: "Compra inválida"
        });
    }

    const newPurchase = {
        id: "TS-" + Date.now(),
        kit: purchase.kit || "DESCONOCIDO",
        minecraft: purchase.minecraft || "",
        discord: purchase.discord || "",
        payment: purchase.payment || "",
        status: "PENDIENTE",
        key: null,
        createdAt: new Date().toLocaleString("es-EC")
    };

    purchases.push(newPurchase);

    console.log("🛒 NUEVA COMPRA:");
    console.log(newPurchase);

    res.json({
        success: true,
        purchase: newPurchase
    });

});


// =========================
// VER COMPRAS
// =========================

app.get("/api/purchases", (req, res) => {

    res.json(purchases);

});


// =========================
// PÁGINA PRINCIPAL
// =========================

app.get("/", (req, res) => {

    res.sendFile(
        path.join(__dirname, "public", "index.html")
    );

});


// =========================
// INICIAR SERVIDOR
// =========================

app.listen(PORT, () => {

    console.log("=================================");
    console.log("⚔️ TS CRAFT SHOP");
    console.log("🚀 Servidor iniciado");
    console.log("🌐 Puerto:", PORT);
    console.log("=================================");

});
